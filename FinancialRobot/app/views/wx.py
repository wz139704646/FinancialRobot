from flask import Blueprint, render_template, request
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
    password = request.form.get("passwd")
    print(password)
    password = base64.b64decode(str(password, 'utf-8'))
    companyId = request.form.get("companyId")
    helper = MyHelper()
    row = helper.executeUpdate("insert into User (account, password, CompanyId) values (%s,%s,%s)",
                               [account, password, companyId])
    if row == 1:
        return True
    else:
        return False


@wx.route("/login", methods=['POST'])
def login():
    return render_template("login.html")
