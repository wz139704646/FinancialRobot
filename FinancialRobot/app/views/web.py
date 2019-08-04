#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, request
from app.utils.DBHelper import MyHelper
from app.dao.CompanyDao import CompanyDao
from app.dao.SupplierDao import SupplierDao
from app.dao.CustomerDao import CustomerDao
from app.utils.json_util import *
import uuid
import datetime
import time
import json

web = Blueprint("web", __name__)


# 注册公司
@web.route("/CompanyRegister", methods=["GET", "POST"])
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
@web.route("/query_Company", methods=["GET"])
def query_Company():
    query = CompanyDao()
    result = query.queryAll()
    return json.dumps(return_success(CompanyDao.to_dict(result)), ensure_ascii=False)


# 增加供应商
@web.route("/addSupplier", methods=["POST"])
def add_Supplier():
    supquery = SupplierDao()
    _json = request.json
    supname = _json['name']
    supcid = _json['companyId']
    supid = str(uuid.uuid3(uuid.NAMESPACE_OID, supname))
    supphone = _json['phone']
    site = _json['site']
    taxpayerNumber = _json['taxpayerNumber']
    bankname = _json['bankname']
    bankaccount = _json['bankaccount']
    row = supquery.add(supid, supname, supphone, site, taxpayerNumber, bankaccount, bankname, supcid)
    if row == 1:
        return json.dumps(return_success(supid))
    else:
        return json.dumps(return_unsuccess('Error: Add false'))


# 查询所有供应商
@web.route("/queryAllSupplier", methods=["POST"])
def query_AllSupplier():
    queryAllsup = SupplierDao()
    supresult = queryAllsup.queryAll()
    return json.dumps(return_success(SupplierDao.to_dict(supresult)), ensure_ascii=False)


# 根据公司id查询供应商
@web.route("/queryByCompanyId", methods=["POST"])
def query_Supplier_Bycid():
    supqueryBycid = SupplierDao()
    _sjson = request.json
    supCid = _sjson['companyId']
    supQueryresult = supqueryBycid.query_byCompanyId(supCid)
    size = len(supQueryresult)
    if size == 0:
        return json.dumps(return_unsuccess('Error: No data'))
    else:
        return json.dumps(return_success(SupplierDao.to_dict(supQueryresult)), ensure_ascii=False)


# 增加客户
@web.route("/addCustomer", methods=["POST"])
def AddCustomer():
    _json = request.json
    companyId = _json['companyId']
    name = _json['name']
    ID = str(uuid.uuid3(uuid.NAMESPACE_OID, name))
    phone = _json['phone']
    bankAccount = _json['bankAccount']
    bankname = _json['bankname']
    credit = "良好"
    addCustomer = CustomerDao()
    row = addCustomer.add(ID, name, phone, credit, companyId, bankname, bankAccount)
    if row == 1:
        return json.dumps(return_success(ID))
    else:
        return json.dumps(return_unsuccess('Error: Add failed'))


# 客户列表
@web.route("/queryAllCustomer", methods=["POST"])
def query_AllCustomer():
    queryAllCus = CustomerDao()
    _json = request.json
    companyId = _json['companyId']
    Cusresult = queryAllCus.query_byCompanyId(companyId)
    size = len(Cusresult)
    if size == 0:
        return json.dumps(return_unsuccess('Error: No data'))
    else:
        return json.dumps(return_success(CustomerDao.to_dict(Cusresult)), ensure_ascii=False)


# 查询客户
@web.route("/queryCustomer", methods=["POST"])
def queryCustomer():
    query = CustomerDao()
    _json = request.json
    companyId = _json['companyId']
    if _json.get('name') == None:
        if _json.get('phone') == None:
            Cusresult = query.query_byCompanyId(companyId)
            size = len(Cusresult)
            if size == 0:
                return json.dumps(return_unsuccess('Error: No data'))
            else:
                return json.dumps(return_success(CustomerDao.to_dict(Cusresult)), ensure_ascii=False)
        else:
            phone = _json['phone']
            newphone = '%' + phone + '%'
            Cusresult = query.query_by_phone(companyId, newphone)
            size = len(Cusresult)
            if size == 0:
                return json.dumps(return_unsuccess('Error: No data'))
            else:
                return json.dumps(return_success(CustomerDao.to_dict(Cusresult)), ensure_ascii=False)

    else:
        name = _json['name']
        newname = '%' + name + '%'
        Cusresult = query.query_by_phone(companyId, newname)
        size = len(Cusresult)
        if size == 0:
            return json.dumps(return_unsuccess('Error: No data'))
        else:
            return json.dumps(return_success(CustomerDao.to_dict(Cusresult)), ensure_ascii=False)


# 根据Id查询供应商名称
@web.route("/querySupplierById", methods=["POST"])
def querySupplierById():
    query = SupplierDao()
    _json = request.json
    id = _json.get('id')
    result = query.query_byId(id)
    size = len(result)
    if size == 0:
        return json.dumps(return_unsuccess('Error: No data'))
    else:
        return json.dumps(return_success(SupplierDao.to_dict(result)), ensure_ascii=False, cls=DecimalEncoder)


# 根据Id查询客户
@web.route("/queryCustomerById", methods=["POST"])
def queryCustomerById():
    query = CustomerDao()
    _json = request.json
    id = _json.get('id')
    result = query.query_byId(id)
    size = len(result)
    if size == 0:
        return json.dumps(return_unsuccess('Error: No data'))
    else:
        return json.dumps(return_success(CustomerDao.to_dict(result)), ensure_ascii=False, cls=DecimalEncoder)
