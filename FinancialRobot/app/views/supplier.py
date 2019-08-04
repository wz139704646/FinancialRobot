#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, request
from app.dao.SupplierDao import SupplierDao
from app.utils.json_util import *
import uuid
import json

supplier = Blueprint("supplier", __name__)
# 增加供应商
@supplier.route("/addSupplier", methods=["POST"])
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
@supplier.route("/queryAllSupplier", methods=["POST"])
def query_AllSupplier():
    queryAllsup = SupplierDao()
    supresult = queryAllsup.queryAll()
    return json.dumps(return_success(SupplierDao.to_dict(supresult)), ensure_ascii=False)

# 根据公司id查询供应商
@supplier.route("/queryByCompanyId", methods=["POST"])
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




# 根据Id查询供应商名称
@supplier.route("/querySupplierById", methods=["POST"])
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


