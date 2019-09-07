import time
import uuid
from flask import Blueprint, render_template, request, session, jsonify
from app.utils.DBHelper import MyHelper
from app.dao.PurchaseDao import PurchaseDao
from app.dao.SupplierDao import SupplierDao
from app.dao.GoodsDao import GoodsDao
from app.utils.auth import check_token
from app.utils.json_util import *

purchase = Blueprint("purchase", __name__)
purchase.secret_key = 'secret_key_purchase'


@purchase.before_request
@check_token
def res():
    pass


# 登记进货
@purchase.route("/addPurchase", methods=["POST"])
def addPurchase():
    conn = MyHelper()
    _json = request.json
    params = []
    sqls = []
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
        params.append([id, goodsId, goodsName, provideNo, companyId, number, purchasePrice, date, "运"])
        sqls.append(
            "insert into Purchase (id,goodId, goodName, supplierId, companyId, number, purchasePrice, date,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    rows = conn.executeUpdateTransaction(sqls=sqls, params=params)
    if rows:
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
    querySupplierName = SupplierDao()
    queryGoodsPhoto = GoodsDao()
    _json = request.json
    companyId = _json.get('companyId')
    results = []
    if _json.get('id') == None:
        if _json.get('date') == None:
            idResult = query.queryAllId(companyId)
        else:
            if _json.get('start') != None:
                start = _json.get('start')
                end = _json.get('end')
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
                    PhothResult = queryGoodsPhoto.query_byId(goodsResult[i][1])
                    goodsPhoto = PhothResult[0][7]
                    NameResult = querySupplierName.query_byId(supplierId)
                    supplierName = NameResult[0][1]
                    date = goodsResult[i][7]
                    goods = []
                    goods.append(goodsResult[i][6])
                    goods.append(goodsResult[i][1])
                    goods.append(goodsPhoto)
                    goods.append(goodsResult[i][2])
                    goods.append(goodsResult[i][5])
                    goodsList.append(goods)
                result.append(id)
                result.append(status)
                result.append(supplierId)
                result.append(date)
                result.append(supplierName)
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
            PhothResult = queryGoodsPhoto.query_byId(goodsResult[i][1])
            goodsPhoto = PhothResult[0][7]
            NameResult = querySupplierName.query_byId(supplierId)
            supplierName = NameResult[0][1]
            date = goodsResult[i][7]
            goods = []
            goods.append(goodsResult[i][6])
            goods.append(goodsResult[i][1])
            goods.append(goodsPhoto)
            goods.append(goodsResult[i][2])
            goods.append(goodsResult[i][5])
            goodsList.append(goods)
        result.append(id)
        result.append(status)
        result.append(supplierId)
        result.append(date)
        result.append(supplierName)
        result.append(goodsList)
        results.append(result)
    size = len(results)
    if size == 0:
        return json.dumps(return_unsuccess('Error: No data'))
    else:
        return json.dumps(return_success(PurchaseDao.to_dict(results)), ensure_ascii=False, cls=DecimalEncoder)


# 查询商品进货价格
@purchase.route("/purchasePriceByName", methods=["POST"])
def purchasePriceByName():
    query = PurchaseDao()
    _json = request.json
    name = _json.get('name')
    newname = '%' + name + '%'
    result1 = query.purchasePriceByName(newname)
    size = len(result1)
    if size >= 1:
        result = []
        for row in result1:
            res = {}
            res['purchasePrice'] = row[0]
            res['date'] = row[1]
            result.append(res)
        return json.dumps(return_success(result), ensure_ascii=False, cls=DecimalEncoder)
    else:
        return json.dumps(return_unsuccess('Error: No data'))
