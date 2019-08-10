#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, request
from app.dao.CustomerDao import CustomerDao
from app.utils.json_util import *
import uuid
import json

customer = Blueprint("customer", __name__)


# 增加客户
@customer.route("/addCustomer", methods=["POST"])
def addCustomer():
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
@customer.route("/queryAllCustomer", methods=["POST"])
def queryAllCustomer():
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
@customer.route("/queryCustomer", methods=["POST"])
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
        print(name)
        Cusresult = query.queryCustomerByName(companyId, newname)
        size = len(Cusresult)
        if size == 0:
            return json.dumps(return_unsuccess('Error: No data'))
        else:
            return json.dumps(return_success(CustomerDao.to_dict(Cusresult)), ensure_ascii=False)


# 根据Id查询客户
@customer.route("/queryCustomerById", methods=["POST"])
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


# 根据名称查询客户
@customer.route("/queryCustomerByName", methods=["POST"])
def queryCustomerByName():
    _json = request.json
    query = CustomerDao()
    name = _json.get('name')
    companyId = _json.get('companyId')
    print(name, companyId)
    result = query.queryCustomerByName(companyId, name)
    print(result)

    size = len(result)
    if size == 0:
        return json.dumps(return_unsuccess('Error: No data'))
    else:
        return json.dumps(return_success(CustomerDao.to_dict(result)), ensure_ascii=False, cls=DecimalEncoder)
