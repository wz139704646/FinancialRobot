import binascii
from flask import Blueprint, render_template, request, session, jsonify
import json
import base64
from app.dao.GoodsDao import GoodsDao
from app.dao.UserDao import UserDao
from app.utils.DBHelper import MyHelper
from app.utils.decimal_encoder import DecimalEncoder
from app.utils.res_json import *
from app.utils.permissions import check_token
from app.utils import util
from time import time
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
import random
from app.config import redis_store


wx = Blueprint("wx", __name__)
wx.secret_key = 'secret_key_1'

due = 5*60


@wx.route("/")
def hello():
    return render_template("index.html")


@wx.route("/userRegister", methods=["POST"])

def userRegister():
    _json = request.json
    print(_json)
    # account = _json["account"]
    # companyId = _json["companyId"]
    # password = _json["passwd"]
    openid = _json.get("openid")
    # try:
    #     openid = _json["openid"]
    # except KeyError:
    #     openid = None
    account = _json.get("account")
    companyId = _json.get("companyId")
    password = _json.get("passwd")
    verification = _json.get("verification")

    # 验证码验证
    # TODO
    true_veri = redis_store.get('veri'+account)
    print(true_veri)
    print(type(true_veri))
    if not true_veri:
        return jsonify(return_unsuccess("验证码过期"))
    elif verification != true_veri:
        return jsonify(return_unsuccess("验证码错误"))
    # 验证码正确，删除对应键值
    redis_store.delete('veri'+account)

    # 生成token
    login_time = int(time())
    token = util.create_jwt({'account': account, 'login_time': login_time})

    # 密码处理
    store = base64.b64decode(password)
    store_in = binascii.hexlify(store)
    strpass = str(store_in, 'utf-8')
    print(strpass)
    user_dao = UserDao()
    row = user_dao.add(account, strpass, companyId)
    if row == 1:
        resp = return_success("")
        resp['token'] = token
        return jsonify(resp)
    else:
        return json.dumps(return_unsuccess("注册失败"))


@wx.route("/checkAccount")
def check_account():
    account = request.json['account']
    # 到数据库中进行查询
    user_dao = UserDao()
    result = user_dao.query_by_account(account)
    size = len(result)
    if size == 0:
        return json.dumps(return_success(""))
    else:
        return json.dumps(return_unsuccess("Error Account Duplicate"))


@wx.route("/login", methods=['POST'])
def login():
    _json = request.json
    login_type = _json['type']
    # 账号密码登陆
    account = _json['account']
    password = _json['passwd']
    login_time = int(time())
    token = util.create_jwt({'account': account, 'login_time': login_time})
    if login_type == 0:
        store = base64.b64decode(password)
        store_in = binascii.hexlify(store)
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
            return jsonify(return_unsuccess('Error: No such user'))
    # 验证码登陆
    else:
        true_veri = redis_store.get('veri'+account)
        if not true_veri:
            return jsonify(return_unsuccess("验证码过期"))
        elif password != true_veri:
            return jsonify(return_unsuccess("验证码错误"))
        res = json.loads(check_account())
        suc = res.get("success")
        if not suc:
            redis_store.delete('veri'+account)
            resp = return_success(UserDao.to_dict(res))
            resp['token'] = token
        else:
            resp = return_unsuccess('Error: No such user')
        return jsonify(resp)


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
    row = user_dao.bind_wx(_account, _openid)
    if row == 1:
        return json.dumps(return_success(""))
    else:
        return json.dumps(return_unsuccess("Bind Failed"))


@wx.route("/addGoods", methods=['POST'])
def addGoods():
    _json = request.json
    print(_json)
    goods_dao = GoodsDao()
    res = goods_dao.add(_json.get('name'), _json.get('sellprice'), _json.get('companyId'),
                        _json.get('type'), _json.get('unitInfo'))
    if res["row"] == 1:
        return json.dumps(return_success({"id": res["id"]}))
    else:
        return json.dumps(return_unsuccess("添加商品失败"), ensure_ascii=False)


@wx.route("/queryGoods", methods=['POST'])
def queryGoods():
    _json = request.json
    companyId = _json.get('companyId')
    name = _json.get('name')
    type = _json.get('type')
    goods_dao = GoodsDao()
    result = goods_dao.query_by_companyId(companyId, name, type)
    size = len(result)
    if size >= 0:
        return json.dumps(return_success({'goodsList': GoodsDao.to_dict(result)}),
                          cls=DecimalEncoder, ensure_ascii=False)
    else:
        return json.dumps(return_unsuccess("查询失败"), ensure_ascii=False)


@wx.route("/getVerification", methods=['POST'])
def getVerification():
    appid = 1400226777
    appkey = '8e4b05566cb1021da046f438b5db2736'
    phonenumber = request.json.get('account')
    type = request.json.get('type')
    ssender = SmsSingleSender(appid, appkey)
    template_id = 363932
    sms_sign = 'Fbot小程序 '

    if type == 0:
        stype = '登录'
    else:
        stype = '注册'

    # 生成验证码，使用redis缓存，并设置过期时间
    veri = ""
    for i in range(6):
        veri += str(random.randint(0, 9))
    redis_store.set('veri'+phonenumber, veri)
    redis_store.expire('veri'+phonenumber, due)

    params = [stype, veri, round(due/60)]
    try:
        result = ssender.send_with_param(nationcode=86, phone_number=phonenumber, template_id=template_id, params=params, sign=sms_sign, extend="", ext="")
    except HTTPError as e:
        print(e)
    except Exception as e:
        print(e)

    try:
        print(result)
    except Exception as e:
        print(e)

    # print(result)
    return jsonify({'success': True, 'errMsg': '验证码发送完成'})