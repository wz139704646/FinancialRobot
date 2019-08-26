import binascii
from flask import Blueprint, render_template, request, session, jsonify
import json
import base64
from app.dao.UserDao import UserDao
from app.utils.features import get_roles
from app.utils.json_util import *
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
import random
import time
from app.config import redis_store
from app.utils.auth import *

wx = Blueprint("wx", __name__)
wx.secret_key = 'secret_key_1'

due = 5 * 60


@wx.route("/")
def hello():
    return render_template("index.html")


@wx.route("/decodeToken", methods=["POST"])
def decode_token():
    token = request.headers.get('Authorization')
    if not token:
        _json = request.json
        token = _json.get('token')
    token_arr = token.split(' ')
    if (not token_arr) or (token_arr[0] != "JWT") or (len(token_arr) != 2):
        return json.dumps(return_unsuccess('验证头信息不正确'), ensure_ascii=False)
    else:
        auth_token = token_arr[1]
        try:
            data = Auth.decode_jwt(auth_token).get('data')
        except Exception as e:
            return json.dumps(return_unsuccess('token解码失败: ' + str(e)), ensure_ascii=False)
        else:
            account = data.get('account')
            user_dao = UserDao()
            try:
                res = user_dao.query_by_account(account)
                if len(res) == 1:
                    return json.dumps(return_success(UserDao.to_dict(res)), ensure_ascii=False)
                else:
                    return json.dumps((return_unsuccess("Error: No such user")))
            except Exception as e:
                return json.dumps((return_unsuccess("Error: " + str(e))))


@wx.route('/setPosition', methods=["POST"])
def set_position():
    _json = request.json
    account = _json.get("account")
    position = _json.get('position')
    try:
        UserDao().set_position(account, position)
        return json.dumps(return_success('Set position success'))
    except Exception as e:
        return json.dumps(return_unsuccess('Failed to set position ' + str(e)))


@wx.route('/getPosition', methods=['POST', 'GET'])
def get_position():
    return json.dumps(return_success(get_roles()))


@wx.route("/userRegister", methods=["POST"])
def userRegister():
    _json = request.json
    account = _json.get("account")
    res = json.loads(check_account())
    suc = res.get("success")
    if not suc:
        return jsonify(return_unsuccess("账户重复"))

    companyId = _json.get("companyId")
    password = _json.get("passwd")
    verification = _json.get("verification")

    # 验证码验证
    true_veri = redis_store.get('veri' + account)
    print(true_veri)
    print(type(true_veri))
    if not true_veri:
        return jsonify(return_unsuccess("验证码过期"))
    elif verification != true_veri:
        return jsonify(return_unsuccess("验证码错误"))
    # 验证码正确，删除对应键值
    redis_store.delete('veri' + account)

    # 生成token
    login_time = int(time.time())
    token = Auth.create_jwt({'account': account, 'login_time': login_time})

    # 密码处理
    store = base64.b64decode(password)
    store_in = binascii.hexlify(store)
    strpass = str(store_in, 'utf-8')
    print(strpass)
    try:
        user_dao = UserDao()
        user_dao.add(account, strpass, companyId)
        resp = return_success("")
        resp['token'] = token
        return jsonify(resp)
    except Exception as e:
        print(e)
        return json.dumps(return_unsuccess("注册失败"), ensure_ascii=False)


@wx.route("/checkAccount")
def check_account():
    account = request.json.get('account')
    # 到数据库中进行查询
    user_dao = UserDao()
    result = user_dao.query_by_account(account)
    size = len(result)
    if size == 0:
        return json.dumps(return_success(""))
    else:
        return json.dumps(return_unsuccess("Error Account Duplicate"))


@wx.route("/login", methods=['POST', 'GET'])
def login():
    # token登陆
    print(request.method)
    if request.method == 'GET':
        return decode_token()

    _json = request.json
    login_type = _json.get('type')
    account = _json.get('account')
    password = _json.get('passwd')
    web = _json.get('web')
    # 生成token
    login_time = int(time.time())
    token = Auth.create_jwt({'account': account, 'login_time': login_time})
    # 账号密码登陆
    if login_type == 0:
        store_in = base64.b64decode(password)
        if not web:
            store_in = binascii.hexlify(store_in)
        strpass = str(store_in, 'utf-8')
        print(strpass)

        user_dao = UserDao()
        res = user_dao.query_check_login(account, strpass)
        size = len(res)
        if size == 1:
            resp = return_success(UserDao.to_dict(res))
            resp['token'] = token
            return jsonify(resp)
        else:
            return jsonify(return_unsuccess('账号或密码错误'))
    # 验证码登陆
    elif login_type == 1:
        true_veri = redis_store.get('veri' + account)
        if not true_veri:
            return jsonify(return_unsuccess("验证码过期"))
        elif password != true_veri:
            return jsonify(return_unsuccess("验证码错误"))
        res = json.loads(check_account())
        suc = res.get("success")
        if not suc:
            print(res)
            redis_store.delete('veri' + account)
            user = UserDao().query_by_account(account)
            resp = return_success(UserDao.to_dict(user))
            resp['token'] = token
        else:
            resp = return_unsuccess('Error: No such user')
        return jsonify(resp)
    # openid登陆
    elif login_type == 2:
        openid = _json.get("openid")
        user_dao = UserDao()
        res = user_dao.query_by_openid_account(account, openid)
        size = len(res)
        if size == 1:
            resp = return_success(UserDao.to_dict(res))
            token = Auth.create_jwt({'account': res[0][0], 'login_time': login_time})
            resp['token'] = token
            return jsonify(resp)
        else:
            return jsonify(return_unsuccess('Error: No such user'))
    else:
        return jsonify(return_unsuccess('Error: Wrong Login Method'))


@wx.route("/getVerification", methods=['POST'])
def getVerification():
    appid = 1400226777
    appkey = '8e4b05566cb1021da046f438b5db2736'
    phonenumber = request.json.get('account')
    type = request.json.get('type')
    ssender = SmsSingleSender(appid, appkey)
    template_id = 363932
    sms_sign = 'Fibot小程序 '

    if type == 0:
        stype = '登录'
    else:
        stype = '注册'

    # 生成验证码，使用redis缓存，并设置过期时间
    veri = ""
    for i in range(6):
        veri += str(random.randint(0, 9))
    redis_store.set('veri' + phonenumber, veri)
    redis_store.expire('veri' + phonenumber, due)

    params = [stype, veri, round(due / 60)]
    try:
        result = ssender.send_with_param(nationcode=86, phone_number=phonenumber, template_id=template_id,
                                         params=params, sign=sms_sign, extend="", ext="")
    except HTTPError as e:
        print(e)
    except Exception as e:
        print(e)

    try:
        print(result)
    except Exception as e:
        print(e)
        return jsonify({'success': True, 'errMsg': '出现未知错误'})
    if result.get('result') == 0:
        return jsonify({'success': True, 'errMsg': '验证码发送完成'})
    else:
        return jsonify({'success': False, 'errMsg': result.get('errMsg')})


@wx.route("/queryUser", methods=["POST"])
def queryUser():
    _openid = request.json.get('openid')
    _account = request.json.get('account')
    user_dao = UserDao()
    res = user_dao.query_by_openid_account(_account, _openid)
    size = len(res)
    if size > 0:
        return json.dumps(return_success(UserDao.to_dict(res)))
    else:
        return json.dumps(return_unsuccess('Error: No such user'))


@wx.route("/bindUserWx", methods=["POST"])
def bindUserWx():
    _openid = request.json.get('openid')
    _account = request.json.get('account')
    user_dao = UserDao()
    try:
        user_dao.bind_wx(_account, _openid)
        return json.dumps(return_success(""))
    except Exception as e:
        return json.dumps(return_unsuccess("Bind Failed " + str(e)))
