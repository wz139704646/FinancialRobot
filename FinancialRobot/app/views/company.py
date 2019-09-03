#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, request
from app.utils.DBHelper import MyHelper
from app.dao.CompanyDao import CompanyDao
from app.utils.auth import check_token
from app.utils.json_util import *
import uuid
import json

company = Blueprint("company", __name__)


@company.before_request
@check_token
def res():
    pass


# 注册公司
@company.route("/CompanyRegister", methods=["GET", "POST"])
def CompanyRegister():
    if request.method == 'GET':
        return render_template("RegisterCompany.html")
    else:
        companyname = request.form.get("companyname")
        place = request.form.get("place")
        helper = MyHelper()
        id = str(uuid.uuid3(uuid.NAMESPACE_OID, companyname))
        row = helper.executeUpdate("insert into Company (id, name, place) values (%s,%s,%s)",
                                   [id, companyname, place])
        if row == 1:
            return render_template("RegisterCompany.html")
        else:
            return False


# 查询公司列表
@company.route("/query_Company", methods=["GET"])
def queryCompany():
    query = CompanyDao()
    result = query.queryAll()
    return json.dumps(return_success(CompanyDao.to_dict(result)), ensure_ascii=False)


# 查询公司名称
@company.route("/query_CompanyName", methods=["GET"])
def queryCompanyName():
    query = CompanyDao()
    _json = request.json
    id = _json.get('id')
    result = query.queryNameById(id)
    return json.dumps(return_success(result[0][0]), ensure_ascii=False)
