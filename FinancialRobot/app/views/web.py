#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, request
from app.utils.DBHelper import MyHelper
web = Blueprint("web", __name__)

@web.route("/CompanyRegister", methods=["GET","POST"])
def CompanyRegister():
    if request.method=='GET':
       return render_template("RegisterCompany.html")
    else:
       companyname = request.form.get("companyname")
       place = request.form.get("place")
       print(companyname)
       print(place)
       helper = MyHelper()
       id="4"
       row = helper.executeUpdate("insert into Company (id, name, place) values (%s,%s,%s)",
                               [id, companyname, place])
       if row == 1:
           return render_template("RegisterCompany.html")
       else:
           return False

