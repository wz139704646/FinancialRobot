import time
import uuid
from flask import Blueprint, render_template, request, session, jsonify
from app.dao.CustomerDao import CustomerDao
from app.dao.GoodsDao import GoodsDao
from app.dao.SellDao import SellDao
from app.utils.json_util import *

sell = Blueprint("sell", __name__)
sell.secret_key = 'secret_key_sell'


# 插入销售记录
@sell.route("/addSell", methods=["POST"])
def addSell():
    query = SellDao()
    queryCustomer = CustomerDao()
    queryGoods = GoodsDao()
    _json = request.json
    rows=[]
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
        rows.append(row)
    length=0
    for arow in rows:
        length+=arow
    if length == len(goodsList):
        return json.dumps(return_success(id))
    else:
        return json.dumps(return_unsuccess('Error: Add failed'))

# 查询销售记录
@sell.route("/querySell", methods=["POST"])
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
