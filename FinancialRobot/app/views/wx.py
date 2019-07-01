import binascii

from flask import Blueprint, render_template, request, session
from hashlib import sha1
import json
import base64

from app.dao.UserDao import UserDao
from app.utils.DBHelper import MyHelper

wx = Blueprint("wx", __name__)
wx.secret_key = 'secret_key_1'


@wx.route("/")
def hello():
    return render_template("index.html")


@wx.route("/userRegister", methods=["POST"])
def userRegister():
    account = request.form.get("account")
    companyId = request.form.get("companyId")
    password = request.form.get("passwd")
    store = base64.b64decode(password)
    store_in = binascii.hexlify(store)
    strpass = str(store_in, 'utf-8')
    print(strpass)
    user_dao = UserDao()
    row = user_dao.add(account, strpass, companyId)
    if row == 1:
        return True
    else:
        return False


@wx.route("/checkAccount")
def check_account():
    account = request.args.get("account")
    # 到数据库中进行查询
    user_dao = UserDao()
    result = user_dao.query_by_account(account)
    size = len(result)
    if size == 0:
        return True
    else:
        return False


@wx.route("/login", methods=['POST'])
def login():
    login_type = request.form['type']
    if login_type == 0:
        account = request.form.get("account")
        password = request.form.get("passwd")
        store = base64.b64decode(password)
        store_in = binascii.hexlify(store)
        strpass = str(store_in, 'utf-8')
        print(strpass)

        user_dao = UserDao()
        result = user_dao.query_check_login(account, strpass)
        size = len(result)
        if size == 1:
            return json.dumps(UserDao.to_dict(result))

        else:
            return False

