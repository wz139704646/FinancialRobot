import binascii

from flask import Blueprint, render_template, request, session
from hashlib import sha1
import json
import base64

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
    helper = MyHelper()
    row = helper.executeUpdate("insert into User (account, password, CompanyId) values (%s,%s,%s)",
                               [account, strpass, companyId])
    if row == 1:
        return True
    else:
        return False


@wx.route("/checkAccount")
def checkAccount():
    account = request.args.get("account")
    # 到数据库中进行查询
    helper = MyHelper()
    result = helper.executeQuery("select * from User where account=%s", [account])
    size = len(result)
    if size == 0:
        return True
    else:
        return False


@wx.route("/login", methods=['POST'])
def login():
    account = request.form.get("account")
    password = request.form.get("passwd")
    store = base64.b64decode(password)
    store_in = binascii.hexlify(store)
    strpass=str(store_in,'utf-8')
    print(strpass)

    helper = MyHelper()
    result = helper.executeQuery("select * from User where account=%s and password=%s ",
                                 [account, strpass])
    size = len(result)
    if size == 1:
        # (())
        # 获取用户id
        uid = result[0][0]
        # 将用户id保存到会话中
        session['uid'] = uid
        r = helper.executeQuery("select * from goods where uid=%s", [uid])
        return render_template("index.html", r=r)

    else:
        return render_template("login.html")
