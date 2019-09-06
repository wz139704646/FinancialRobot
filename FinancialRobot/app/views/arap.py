import requests
from flask import Flask, request, redirect, Blueprint

from app.dao.PurchaseDao import PurchaseDao
from app.dao.SellDao import SellDao
from app.utils.auth import *
from app.utils.json_util import *
from app.dao.ARAPDao import ARAPDao

arap = Blueprint("arap", __name__)
arap.secret_key = 'arapxxxx'

clear_forms = ['现金', '支票', '银行转账', '网上支付']
bank_names = ['花旗银行', '中国银行', '中国工商银行', '中国农业银行', '中国建设银行', '交通银行']
_uri = 'https://www.fibot.cn'
# _uri = 'http://127.0.0.1:5000'


@arap.before_request
@check_token
def res():
    pass
    # print(request.path)
    # print(request.endpoint)


@arap.route('/getPayMethods', methods=['POST', 'GET'])
def get_pay_methods():
    return json.dumps(return_success(clear_forms))


@arap.route('/getBankNames', methods=['POST', 'GET'])
def get_bank_names():
    return json.dumps(return_success(bank_names))


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
    _bank_name = _json.get('bankName')
    _clear_form = _json.get('clearForm')
    try:
        arap = ARAPDao()
        res = arap.add_payment(_id, _amount, _date, _bank_name, _clear_form)
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
        receive_info = arap.check_payment(_id)
        info = ARAPDao.to_pay_dict(receive_info)[0]
        clear_form = info.get('clear_form')
        headers = {'Authorization': request.headers.get('Authorization'),
                   'Content-Type': 'application/json'}
        if clear_form == '现金':
            url = _uri + '/addCashRecord'
            _json = {
                'date': info.get('date'),
                'variation': -info.get('pay'),
                'changeDescription': '付款'
            }
        else:
            url = _uri + '/addBankRecord'
            _supplier_id = PurchaseDao().query_byId(info.get('purchaseId'))[0][3]
            _json = {
                'voucher': info.get('id'),
                'date': info.get('date'),
                'amount': -info.get('pay'),
                'bankName': info.get('bank_name'),
                'customerId': _supplier_id,
                'clearForm': info.get('clear_form')
            }
        _json = json.dumps(_json, ensure_ascii=False, cls=DecimalEncoder)
        response = requests.post(url, data=_json.encode('utf-8'),
                                 headers=headers)
        return response.content
    except Exception as e:
        print(e)
        return json.dumps(return_unsuccess('Check Error: ' + str(e)))


@arap.route('/addReceive', methods=['POST'])
def addReceive():
    _json = request.json
    _id = _json.get('sellId')
    _amount = _json.get('amount')
    _date = _json.get('date')
    _bank_name = _json.get('bankName')
    _clear_form = _json.get('clearForm')
    try:
        arap = ARAPDao()
        res = arap.add_receive(_id, _amount, _date, _bank_name, _clear_form)
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
        receive_info = arap.check_receive(_id)
        info = ARAPDao.to_receive_dict(receive_info)[0]
        clear_form = info.get('clear_form')
        headers = {'Authorization': request.headers.get('Authorization'),
                   'Content-Type': 'application/json'}
        if clear_form == '现金':
            url = _uri + '/addCashRecord'
            _json = {
                'date': info.get('date'),
                'variation': info.get('receive'),
                'changeDescription': '收款'
            }
        else:
            url = _uri + '/addBankRecord'
            _customer_id = SellDao().query_byId(info.get('sellId'))[0][1]
            _json = {
                'voucher': info.get('id'),
                'date': info.get('date'),
                'amount': info.get('receive'),
                'bankName': info.get('bank_name'),
                'customerId': _customer_id,
                'clearForm': info.get('clear_form')
            }
        _json = json.dumps(_json, ensure_ascii=False, cls=DecimalEncoder)
        response = requests.post(url, data=_json.encode('utf-8'),
                                 headers=headers)
        return response.content
    except Exception as e:
        return json.dumps(return_unsuccess('Check Error: ' + str(e)))
