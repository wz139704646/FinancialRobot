#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import uuid
from flask import Blueprint, render_template, request, session, jsonify
from app.utils.DBHelper import MyHelper
from app.dao.CustomerDao import CustomerDao
from app.dao.GoodsDao import GoodsDao
from app.dao.SellDao import SellDao
from app.utils.auth import check_token
from app.utils.json_util import *

sell = Blueprint("sell", __name__)
sell.secret_key = 'secret_key_sell'


@sell.before_request
@check_token
def res():
    pass


# 插入销售记录
@sell.route("/addSell", methods=["POST"])
def addSell():
    conn = MyHelper()
    queryCustomer = CustomerDao()
    queryGoods = GoodsDao()
    _json = request.json
    params = []
    sqls = []
    companyId = _json.get('companyId')
    customerId = _json.get('customerId')
    result = queryCustomer.query_byId(customerId)
    if len(result) == 1:
        customerName = result[0][1]
    else:
        customerName = ""
    date = _json.get('date')
    goodsList = _json.get('goodsList')
    id = str(uuid.uuid3(uuid.NAMESPACE_OID, str(time.time())))
    # print(goodsList)
    for puchase in goodsList:
        sumprice = puchase['sumprice']
        goodsId = puchase['goodsId']
        number = puchase['number']
        goodsResult = queryGoods.query_byId(goodsId)
        if len(goodsResult) == 1:
            goodsName = goodsResult[0][1]
            goodsUnit = goodsResult[0][5]
        else:
            goodsName = ""
        params.append([id, customerId, goodsId, companyId, number, sumprice, date, customerName, goodsName, goodsUnit])
        sqls.append(
            "insert into Sell (id,customerId, goodsId, companyId, number, sumprice,date,customerName,goodsName,unitInfo) "
            "values (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s)")

    rows = conn.executeUpdateTransaction(sqls=sqls, params=params)
    if rows:
        return json.dumps(return_success(id))
    else:
        return json.dumps(return_unsuccess('Error: Add failed'))


# 查询销售记录
@sell.route("/querySell", methods=["POST"])
def querySell():
    query = SellDao()
    _json = request.json
    companyId = _json.get('companyId')
    results = []
    if _json.get('date') == None:
        if _json.get('id') == None:
            if _json.get('page') == None:
                return json.dumps(return_unsuccess('Error: Please send page'))
            else:
                page=_json.get('page')
                limit=20
                offset=(page-1)*20
                sumCount=len(query.queryAllId())
                idresult = query.queryGoodsIdByPage(limit,offset)
                if len(idresult) != 0:
                    for j in range(0, len(idresult)):
                        result = []
                        id = idresult[j][0]
                        customerName = ""
                        customerId = ""
                        date = ""
                        goodslist = []
                        goodsResult = query.queryGoodsAllInfo(id)
                        for i in range(0, len(goodsResult)):
                            customerName = goodsResult[i][17]
                            sellStatus = goodsResult[i][20]
                            customerId = goodsResult[i][11]
                            date = goodsResult[i][16]
                            goods = []
                            goods.append(goodsResult[i][12])
                            goods.append(goodsResult[i][15])
                            goods.append(goodsResult[i][14])
                            goods.append(goodsResult[i][18])
                            goods.append(goodsResult[i][7])
                            goodslist.append(goods)
                        result.append(id)
                        result.append(customerId)
                        result.append(customerName)
                        result.append(date)
                        result.append(sumCount)
                        result.append(goodslist)
                        result.append(sellStatus)
                        results.append(result)
        else:
            id = _json.get('id')
            sumCount = 1
            result = []
            customerName = ""
            customerId = ""
            date = ""
            goodslist = []
            goodsResult = query.queryGoodsAllInfoById(id)
            for i in range(0, len(goodsResult)):
                customerName = goodsResult[i][17]
                sellStatus = goodsResult[i][20]
                customerId = goodsResult[i][11]
                date = goodsResult[i][16]
                goods = []
                goods.append(goodsResult[i][12])
                goods.append(goodsResult[i][15])
                goods.append(goodsResult[i][14])
                goods.append(goodsResult[i][18])
                goods.append(goodsResult[i][7])
                goodslist.append(goods)
            result.append(id)
            result.append(customerId)
            result.append(customerName)
            result.append(date)
            result.append(sumCount)
            result.append(goodslist)
            result.append(sellStatus)
            results.append(result)
    else:
        if _json.get('start') == None:
            date = _json.get('date')
            start = datetime.datetime.strptime(date, '%Y-%m-%d')
            delta = datetime.timedelta(days=1)
            n_days = start + delta
            end = n_days.strftime('%Y-%m-%d %H:%M:%S')
        else:
            start = _json.get('start')
            end = _json.get('end')
        idresult = query.query_byDate(companyId, start, end)
        sumCount = len(idresult)

        if sumCount == 0:
            return json.dumps(return_unsuccess('Error: No data'))
        else:
            for j in range(0, len(idresult)):
                result = []
                id = idresult[j][0]
                customerName = ""
                customerId = ""
                date = ""
                goodslist = []
                goodsResult = query.query_byId(id)
                for i in range(0, len(goodsResult)):
                    customerName = goodsResult[i][17]
                    sellStatus = goodsResult[i][20]
                    customerId = goodsResult[i][11]
                    date = goodsResult[i][16]
                    goods = []
                    goods.append(goodsResult[i][12])
                    goods.append(goodsResult[i][15])
                    goods.append(goodsResult[i][14])
                    goods.append(goodsResult[i][18])
                    goods.append(goodsResult[i][7])
                    goodslist.append(goods)
                result.append(id)
                result.append(customerId)
                result.append(customerName)
                result.append(date)
                result.append(sumCount)
                result.append(goodslist)
                result.append(sellStatus)
                results.append(result)
    size = len(results)
    # print(results)
    if size == 0:
        return json.dumps(return_unsuccess('Error: No data'))
    else:
        return json.dumps(return_success(SellDao.to_dict(results)), ensure_ascii=False,
                          cls=DecimalEncoder)


# 根据Id查询销售记录
@sell.route("/querySellById", methods=["POST"])
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


# 查询销售记录
@sell.route("/querySellByDate", methods=["POST"])
def querySellByDate():
    query = SellDao()
    _json = request.json
    companyId = _json.get('companyId')
    start = _json.get('start')
    end = _json.get('end')
    results = []
    idresult = query.query_byDate(companyId, start, end)
    size = len(idresult)
    if size == 0:
        return json.dumps(return_unsuccess('Error: No data'))
    else:
        for j in range(0, len(idresult)):
            result = []
            id = idresult[j][0]
            customerName = ""
            customerId = ""
            date = ""
            goodslist = []
            goodsResult = query.query_byId(id)
            for i in range(0, len(goodsResult)):
                customerName = goodsResult[i][7]
                customerId = goodsResult[i][1]
                date = goodsResult[i][6]
                goods = []
                goods.append(goodsResult[i][2])
                goods.append(goodsResult[i][5])
                goods.append(goodsResult[i][4])
                goods.append(goodsResult[i][8])
                goodslist.append(goods)
            result.append(id)
            result.append(customerId)
            result.append(customerName)
            result.append(date)
            result.append(goodslist)
            results.append(result)
    size = len(results)
    # print(results)
    if size == 0:
        return json.dumps(return_unsuccess('Error: No data'))
    else:
        return json.dumps(return_success(SellDao.to_dict(results)), ensure_ascii=False, cls=DecimalEncoder)


# 查询商品进货价格
@sell.route("/SellPriceByName", methods=["POST"])
def SellPriceByName():
    query = SellDao()
    _json = request.json
    name = _json.get('name')
    newname = '%' + name + '%'
    result1 = query.SellPriceByName(newname)
    size = len(result1)
    if size >= 1:
        result = []
        for row in result1:
            res = {}
            res['number'] = row[0]
            res['sumprice'] = row[1]
            res['date'] = row[2]
            res['goodsName'] = row[3]
            res['customerName'] = row[4]
            result.append(res)
        return json.dumps(return_success(result), ensure_ascii=False, cls=DecimalEncoder)
    else:
        return json.dumps(return_unsuccess('Error: No data'))
