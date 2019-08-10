import time
import uuid
from flask import Blueprint, render_template, request, session, jsonify
from app.dao.PurchaseDao import PurchaseDao
from app.utils.json_util import *

purchase = Blueprint("purchase", __name__)
purchase.secret_key = 'secret_key_purchase'


# 登记进货
@purchase.route("/addPurchase", methods=["POST"])
def addPurchase():
    query = PurchaseDao()
    rows = []
    _json = request.json
    companyId = _json.get('companyId')
    purchases = _json.get('purchases')
    provideNo = _json.get('supplierId')
    date = _json.get('date')
    id = str(uuid.uuid3(uuid.NAMESPACE_OID, str(time.time())))
    print(purchases)
    for puchase in purchases:
        goodsId = puchase['id']
        print(goodsId)
        goodsName = puchase['name']
        print(goodsName)
        number = puchase['buyNum']
        print(number)
        purchasePrice = puchase['price']
        print(purchasePrice)
        row = query.add(id, goodsId, goodsName, provideNo, companyId, number, purchasePrice, date, "运")
        rows.append(row)
    print(rows)
    length = 0
    for arow in rows:
        length += arow
    if length == len(rows):
        return json.dumps(return_success(id))
    else:
        return json.dumps(return_unsuccess('Error: Add failed'))


# 根据Id查询进货记录
@purchase.route("/queryPurchaseById", methods=["POST"])
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


# 查询进货记录
@purchase.route("/queryPurchase", methods=["POST"])
def queryPurchase():
    query = PurchaseDao()
    _json = request.json
    companyId = _json.get('companyId')
    results = []
    if _json.get('id') == None:
        if _json.get('date') == None:
            idResult = query.queryAllId(companyId)
        else:
            date = _json.get('date')
            start = datetime.datetime.strptime(date, '%Y-%m-%d')
            delta = datetime.timedelta(days=1)
            n_days = start + delta
            end = n_days.strftime('%Y-%m-%d %H:%M:%S')
            idResult = query.query_byDate(companyId, start, end)
        size = len(idResult)
        if size == 0:
            return json.dumps(return_unsuccess('Error: No data'))
        else:
            for j in range(0, len(idResult)):
                result = []
                id = idResult[j][0]
                goodsList = []
                goodsResult = query.query_byId(id)
                for i in range(0, len(goodsResult)):
                    status = goodsResult[i][8]
                    supplierId = goodsResult[i][3]
                    date = goodsResult[i][7]
                    goods = []
                    goods.append(goodsResult[i][6])
                    goods.append(goodsResult[i][1])
                    goods.append(goodsResult[i][2])
                    goods.append(goodsResult[i][5])
                    goodsList.append(goods)
                result.append(id)
                result.append(status)
                result.append(supplierId)
                result.append(date)
                result.append(goodsList)
                results.append(result)
    else:
        id = _json.get('id')
        result = []
        goodsList = []
        goodsResult = query.query_byId(id)
        for i in range(0, len(goodsResult)):
            status = goodsResult[i][8]
            supplierId = goodsResult[i][3]
            date = goodsResult[i][7]
            goods = []
            goods.append(goodsResult[i][6])
            goods.append(goodsResult[i][1])
            goods.append(goodsResult[i][2])
            goods.append(goodsResult[i][5])
            goodsList.append(goods)
        result.append(id)
        result.append(status)
        result.append(supplierId)
        result.append(date)
        result.append(goodsList)
        results.append(result)
    size = len(results)
    if size == 0:
        return json.dumps(return_unsuccess('Error: No data'))
    else:
        return json.dumps(return_success(PurchaseDao.to_dict(results)), ensure_ascii=False, cls=DecimalEncoder)
