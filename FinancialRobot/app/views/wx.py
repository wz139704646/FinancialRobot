import binascii
from flask import Blueprint, render_template, request, session
import json
import base64
from app.dao.GoodsDao import GoodsDao
from app.dao.UserDao import UserDao
from app.utils.DBHelper import MyHelper
from app.utils.decimal_encoder import DecimalEncoder
from app.utils.res_json import *

wx = Blueprint("wx", __name__)
wx.secret_key = 'secret_key_1'


@wx.route("/")
def hello():
    return render_template("index.html")


@wx.route("/userRegister", methods=["POST"])
def userRegister():
    _json = request.json
    account = _json["account"]
    companyId = _json["companyId"]
    password = _json["passwd"]
    openid = _json["openid"]
    verification = _json["verification"]
    open

    # 验证码验证
    # TODO

    # 密码处理
    store = base64.b64decode(password)
    store_in = binascii.hexlify(store)
    strpass = str(store_in, 'utf-8')
    print(strpass)
    user_dao = UserDao()
    row = user_dao.add(account, strpass, companyId,openid)
    if row == 1:
        return json.dumps(return_success(""))
    else:
        return json.dumps(return_unsuccess(""))


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
    if login_type == 0:
        account = _json['account']
        password = _json['passwd']
        store = base64.b64decode(password)
        store_in = binascii.hexlify(store)
        strpass = str(store_in, 'utf-8')
        print(strpass)

        user_dao = UserDao()
        res = user_dao.query_check_login(account, strpass)
        size = len(res)
        if size == 1:
            return json.dumps(return_success(UserDao.to_dict(res)))
        else:
            return json.dumps(return_unsuccess('Error: No such user'))
    # 验证码登陆
    else:
        # TODO
        return False


@wx.route("/addGoods", methods=['POST'])
def addGoods():
    _json = request.json
    print(_json)
    goods_dao = GoodsDao()
    row = goods_dao.add(_json['name'], _json['sellprice'], _json['companyId'],
                        _json['type'], _json['unitInfo'])
    if row == 1:
        return json.dumps(return_success(""))
    else:
        return json.dumps(return_unsuccess("添加商品失败"),ensure_ascii=False)


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
        return json.dumps(return_success({'goodsList':GoodsDao.to_dict(result)}),
                          cls=DecimalEncoder, ensure_ascii=False)
    else:
        return json.dumps(return_unsuccess("查询失败"),ensure_ascii=False)
