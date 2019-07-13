#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, request
from app.utils.DBHelper import MyHelper
from app.dao.CompanyDao import CompanyDao
from app.dao.SupplierDao import SupplierDao
from app.dao.CustomerDao import CustomerDao
from app.dao.GoodsDao import GoodsDao
from app.dao.WareHouseDao import WareHouseDao
from app.dao.PurchaseDao import PurchaseDao
from app.dao.SellDao import SellDao
from app.utils.res_json import *
from app.utils.decimal_encoder import DecimalEncoder
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


# 登记进货
@web.route("/addPurchase", methods=["POST"])
def RegisterPurchase():
    query = PurchaseDao()
    _json = request.json
    companyId = _json.get('companyId')
    purchases = _json.get('purchases')
    provideNo = _json.get('supplierId')
    date = _json.get('date')
    id = str(uuid.uuid3(uuid.NAMESPACE_OID, str(time.time())))
    print(purchases)
    for puchase in purchases:
        goodsNo = puchase['id']
        goodsName = puchase['name']
        number = puchase['buyNum']
        purchasePrice = puchase['price']
        row = query.add(id, goodsNo, goodsName, provideNo, companyId, number, purchasePrice, date, "运")

        if row == 1:
            return json.dumps(return_success("Yes!"))
        else:
            return json.dumps(return_unsuccess('Error: Add failed'))


# 查询进货记录
@web.route("/queryPurchase", methods=["POST"])
def queryPurchase():
    query = PurchaseDao()
    _json = request.json
    companyId = _json.get('companyId')
    if _json.get('date') == None:
        result = query.query_byCid(companyId)
        size = len(result)
        if size == 0:
            return json.dumps(return_unsuccess('Error: No data'))
        else:
            return json.dumps(return_success(PurchaseDao.to_dict(result)), ensure_ascii=False, cls=DecimalEncoder)
    else:
        date = _json.get('date')
        start = datetime.datetime.strptime(date, '%Y-%m-%d')
        delta = datetime.timedelta(days=1)
        n_days = start + delta
        end = n_days.strftime('%Y-%m-%d %H:%M:%S')
        result = query.query_byDate(companyId, start, end)
        size = len(result)
        if size == 0:
            return json.dumps(return_unsuccess('Error: No data'))
        else:
            return json.dumps(return_success(PurchaseDao.to_dict(result)), ensure_ascii=False, cls=DecimalEncoder)


# 插入销售记录
@web.route("/addSell", methods=["POST"])
def addSell():
    query = SellDao()
    queryCustomer = CustomerDao()
    queryGoods = GoodsDao()
    _json = request.json
    companyId = _json.get('companyId')
    customerId = _json.get('customerId')
    result = queryCustomer.query_byId(customerId)
    if len(result) == 1:
        customerName = result[0][1]
    else:
        customerName = ""
    sumprice = _json.get('sumprice')
    date = _json.get('date')
    goodsList = _json.get('goodsList')
    id = str(uuid.uuid3(uuid.NAMESPACE_OID, str(time.time())))
    print(goodsList)
    for puchase in goodsList:
        goodsId = puchase['goodsId']
        number = puchase['number']
        goodsResult = queryGoods.query_byId(goodsId)
        if len(goodsResult) == 1:
            goodsName = goodsResult[0][1]
            goodsUnit = goodsResult[0][5]
        else:
            goodsName = ""
        row = query.add(id, customerId, goodsId, companyId, number, sumprice, date, customerName, goodsName,goodsUnit)
        if row == 1:
            return json.dumps(return_success("Yes!"))
        else:
            return json.dumps(return_unsuccess('Error: Add failed'))


# 查询销售记录
@web.route("/querySell", methods=["POST"])
def querySell():
    query = SellDao()
    _json = request.json
    companyId = _json.get('companyId')
    if _json.get('date') == None:
        result = query.query_byCid(companyId)
        size = len(result)
        if size == 0:
            return json.dumps(return_unsuccess('Error: No data'))
        else:
            return json.dumps(return_success(SellDao.to_dict(result)), ensure_ascii=False, cls=DecimalEncoder)
    else:
        date = _json.get('date')
        start = datetime.datetime.strptime(date, '%Y-%m-%d')
        delta = datetime.timedelta(days=1)
        n_days = start + delta
        end = n_days.strftime('%Y-%m-%d %H:%M:%S')
        result = query.query_byDate(companyId, start, end)
        size = len(result)
        if size == 0:
            return json.dumps(return_unsuccess('Error: No data'))
        else:
            return json.dumps(return_success(SellDao.to_dict(result)), ensure_ascii=False, cls=DecimalEncoder)


# 根据Id查询销售记录
@web.route("/querySellById", methods=["POST"])
def querySellById():
    query = SellDao()
    _json = request.json
    id = _json.get('id')
    result = query.query_byId(id)
    size = len(result)
    if size == 0:
        return json.dumps(return_unsuccess('Error: No data'))
    else:
        return json.dumps(return_success(SellDao.to_dict(result)), ensure_ascii=False, cls=DecimalEncoder)


# 根据Id查询进货记录
@web.route("/queryPurchaseById", methods=["POST"])
def queryPurchaseById():
    query = PurchaseDao()
    _json = request.json
    id = _json.get('id')
    result = query.query_byId(id)
    size = len(result)
    if size == 0:
        return json.dumps(return_unsuccess('Error: No data'))
    else:
        return json.dumps(return_success(PurchaseDao.to_dict(result)), ensure_ascii=False, cls=DecimalEncoder)

        # purjson = json.dumps(PurchaseDao.to_dict(result), ensure_ascii=False, cls=DecimalEncoder)
        # return_success(purjson)



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

@web.route("/addWarehouse", methods=["POST"])
def addWarehouse():
    _json = request.json
    companyId = _json['companyId']
    name = _json['name']
    ID = str(uuid.uuid3(uuid.NAMESPACE_OID, name))
    site = _json['site']
    addWarehouse = WareHouseDao()
    row = addWarehouse.add(ID, name, site, companyId)
    if row == 1:
        return json.dumps(return_success(ID))
    else:
        return json.dumps(return_unsuccess('Error: Add failed'))


# 查询仓库
@web.route("/queryWarehouse", methods=["POST"])
def queryWarehouse():
    _json = request.json
    companyId = _json['companyId']
    query = WareHouseDao()
    if _json.get('name') == None:
        Cusresult = query.query_byCompanyId(companyId)
        size = len(Cusresult)
        if size == 0:
            return json.dumps(return_unsuccess('Error: No data'))
        else:
            return json.dumps(return_success(WareHouseDao.to_dict(Cusresult)), ensure_ascii=False)
    else:
        name = _json['name']
        newname = '%' + name + '%'
        Cusresult = query.query_by_name(companyId, newname)
        size = len(Cusresult)
        if size == 0:
            return json.dumps(return_unsuccess('Error: No data'))
        else:
            return json.dumps(return_success(WareHouseDao.to_dict(Cusresult)), ensure_ascii=False)
