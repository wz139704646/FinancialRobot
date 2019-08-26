from flask import Flask, request, redirect, Blueprint
from app.utils.json_util import *
from app.dao.ARAPDao import ARAPDao

arap = Blueprint("arap", __name__)
arap.secret_key = 'arapxxxx'


@arap.route('/addPurchasePay', methods=['POST'])
def addPurchasePay():
    _json = request.json
    _purchaseId = _json.get('purchaseId')
    _reason = _json.get('reason')
    try:
        arap = ARAPDao()
        row = arap.add_purchase_pay(_purchaseId, _reason)
        if row == 1:
            return json.dumps(return_success('ok'), cls=DecimalEncoder)
        else:
            return json.dumps(return_unsuccess('添加应付失败'), ensure_ascii=False)
    except Exception as e:
        print(e)
        return json.dumps(return_unsuccess('添加应付失败: ' + str(e)), ensure_ascii=False)


@arap.route('/queryPurchasePay', methods=['POST'])
def queryPurchasePay():
    _json = request.json
    print(_json)
    _purchaseId = _json.get('purchaseId')
    _days = _json.get('days')
    try:
        arap = ARAPDao()
        res = arap.query_purchase_pay(_purchaseId, _days)
        if res:
            return json.dumps(return_success(ARAPDao.to_purchase_pay_dict(res)),
                              cls=DecimalEncoder, ensure_ascii=False)
        else:
            return json.dumps(return_unsuccess('未查询到相关数据'), ensure_ascii=False)
    except Exception as e:
        print(e)
        return json.dumps(return_unsuccess('Query Error: ' + str(e)))


@arap.route('/addSellReceive', methods=['POST'])
def addSellReceive():
    _json = request.json
    _id = _json.get('sellId')
    _reason = _json.get('reason')
    try:
        arap = ARAPDao()
        row = arap.add_sell_receive(_id, _reason)
        if row == 1:
            return json.dumps(return_success('ok'), cls=DecimalEncoder)
        else:
            return json.dumps(return_unsuccess('添加应收失败'), ensure_ascii=False)
    except Exception as e:
        print(e)
        return json.dumps(return_unsuccess('添加应收失败: ' + str(e)), ensure_ascii=False)


@arap.route('/querySellReceive', methods=['POST'])
def querySellReceive():
    _json = request.json
    print(_json)
    _id = _json.get('sellId')
    _days = _json.get('days')
    try:
        arap = ARAPDao()
        res = arap.query_sell_receive(_id, _days)
        if res:
            return json.dumps(return_success(ARAPDao.to_sell_receive_dict(res)),
                              cls=DecimalEncoder, ensure_ascii=False)
        else:
            return json.dumps(return_unsuccess("No related data"))
    except Exception as e:
        print(e)
        return json.dumps(return_unsuccess('Query Error: ' + str(e)))


@arap.route('/addPayment', methods=['POST'])
def addPayment():
    _json = request.json
    _id = _json.get('purchaseId')
    _amount = _json.get('amount')
    _date = _json.get('date')
    try:
        arap = ARAPDao()
        res = arap.add_payment(_id, _amount, _date)
        if res['row'] == 1:
            return json.dumps(return_success({'paymentId': res['id']}), cls=DecimalEncoder)
        else:
            return json.dumps(return_unsuccess('添加支出失败'), ensure_ascii=False)
    except Exception as e:
        print(e)
        return json.dumps(return_unsuccess('添加支出失败: ' + str(e)), ensure_ascii=False)


@arap.route('/queryPayment', methods=['POST'])
def queryPayment():
    _json = request.json
    _id = _json.get('id')
    _purchaseId = _json.get('purchaseId')
    _days = _json.get('days')
    try:
        arap = ARAPDao()
        res = arap.query_payment(_id, _purchaseId, _days)
        return json.dumps(return_success(ARAPDao.to_pay_dict(res)),
                          cls=DecimalEncoder, ensure_ascii=False)
    except Exception as e:
        print(e)
        return json.dumps(return_unsuccess('Query Error: ' + str(e)))


@arap.route('/checkPayment', methods=['POST'])
def checkPayment():
    _id = request.json.get('id')
    try:
        arap = ARAPDao()
        arap.check_payment(_id)
        return json.dumps(return_success('ok'),
                          cls=DecimalEncoder, ensure_ascii=False)
    except Exception as e:
        print(e)
        return json.dumps(return_unsuccess('Check Error: ' + str(e)))


@arap.route('/addReceive', methods=['POST'])
def addReceive():
    _json = request.json
    _id = _json.get('sellId')
    _amount = _json.get('amount')
    _date = _json.get('date')
    try:
        arap = ARAPDao()
        res = arap.add_receive(_id, _amount, _date)
        if res['row'] == 1:
            return json.dumps(return_success({'receiveId': res['id']}), cls=DecimalEncoder)
        else:
            return json.dumps(return_unsuccess('添加收入失败'), ensure_ascii=False)
    except Exception as e:
        print(e)
        return json.dumps(return_unsuccess('添加收入失败: ' + str(e)), ensure_ascii=False)


@arap.route('/queryReceive', methods=['POST'])
def queryReceive():
    _json = request.json
    _id = _json.get('id')
    _sellId = _json.get('sellId')
    _days = _json.get('days')
    try:
        arap = ARAPDao()
        res = arap.query_receive(_id, _sellId, _days)
        return json.dumps(return_success(ARAPDao.to_receive_dict(res)),
                          cls=DecimalEncoder, ensure_ascii=False)
    except Exception as e:
        return json.dumps(return_unsuccess('Query Error: ' + str(e)))


@arap.route('/checkReceive', methods=['POST'])
def checkReceive():
    _id = request.json.get('id')
    try:
        arap = ARAPDao()
        arap.check_receive(_id)
        return json.dumps(return_success('ok'),
                          cls=DecimalEncoder, ensure_ascii=False)
    except Exception as e:
        return json.dumps(return_unsuccess('Check Error: ' + str(e)))
