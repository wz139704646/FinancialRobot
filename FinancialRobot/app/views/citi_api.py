import base64
import http.client
import uuid
import requests
import json

from app.utils.json_util import *
from flask import Blueprint, render_template, request, session, jsonify, redirect
from urllib import parse
from app.config import redis_store

citi_api = Blueprint("citi_api", __name__)
citi_api.secret_key = 'secret_key_citi_api'

CLIENT_ID = "31b2b8c1-8449-4828-8147-c98799373f2d"
CLIENT_SECRET = "C7jW0pM0tJ5cF7eO0gR6gT7cO8wY2jI5sG8qL0iW7hC4cK4lM3"
SCOPE = "pay_with_points accounts_details_transactions customers_profiles payees personal_domestic_transfers " \
        "internal_domestic_transfers external_domestic_transfers bill_payments Drawees Card_Payments Auto_Debit cards " \
        "onboarding reference_data reset_atm_pin statements_and_advices meta_data "
STATE = "12321"
REDIRECT_URI = "http://47.100.244.29/getAccToken"
INDEX = "http://47.100.244.29"


def get_url(url, parameters):
    """
    拼接url与所带参数
    :param url: {str} 链接
    :param parameters: {dict} 参数
    :return: {str} 拼接后的url
    """
    data = parse.urlencode(parameters)
    return url + "?" + data


# 获取auth 的code
def get_basic_auth():
    secret = CLIENT_ID + ":" + CLIENT_SECRET
    b64secret = base64.b64encode(secret.encode())
    return 'Basic ' + b64secret.decode()


# 获取auth的access token
def get_token_auth():
    access_token = redis_store.get('access_token')
    if access_token:
        return "Bearer " + access_token
    else:
        if json.loads(refreshAccToken())['success']:
            access_token = redis_store.get('access_token')
            return "Bearer " + access_token
        else:
            return json.dumps(return_unsuccess('Refresh token expire'))


def get_headers():
    headers = {
        'authorization': get_token_auth(),
        'client_id': CLIENT_ID,
        'uuid': str(uuid.uuid4()),
        'accept': "application/json",
        'content-type': 'application/json'
    }
    return headers


# 获取授权码
@citi_api.route("/getAuthCode", methods=["GET"])
def getAuthCode():
    url = "https://sandbox.apihub.citi.com/gcb/api/authCode/oauth2/authorize"
    headers = {
        'accept': 'application/json'
    }
    parameters = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'scope': SCOPE,
        'countryCode': 'hk',
        'businessCode': 'GCB',
        'locale': 'en_US',
        'state': STATE,
        'redirect_uri': REDIRECT_URI
    }
    # r = requests.get(url=url, params=parameters, headers=headers)
    auth = get_url(url, parameters)
    return redirect(auth)


# 获取access token
@citi_api.route("/getAccToken", methods=["POST", "GET"])
def getAccToken():
    code = request.args.get('code')
    state = request.args.get('state')
    if not (code and state == STATE):
        return "<h1>Authorization code grant failed !!</h1>"
    url = "https://sandbox.apihub.citi.com/gcb/api/authCode/oauth2/token/hk/gcb"

    payload = "grant_type=authorization_code&code={0}&redirect_uri={1}".format(code, REDIRECT_URI)

    headers = {
        'authorization': get_basic_auth(),
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept': "application/json"
    }

    r = requests.post(url, data=payload, headers=headers)

    dic = json.loads(r.text)
    # print(dic)
    redis_store.set('access_token', dic['access_token'], ex=dic['expires_in'])
    redis_store.set('refresh_token', dic['refresh_token'], ex=dic['refresh_token_expires_in'])

    return redirect(INDEX)


# 更新access token
@citi_api.route('/refreshAccToken', methods=['POST', 'GET'])
def refreshAccToken():
    url = "https://sandbox.apihub.citi.com/gcb/api/authCode/oauth2/refresh"

    payload = "grant_type=refresh_token&refresh_token={0}".format(redis_store.get('refresh_token'))

    headers = {
        'authorization': get_basic_auth(),
        'content-type': "application/x-www-form-urlencoded",
        'accept': "application/json"
    }

    r = requests.post(url, data=payload, headers=headers)
    dic = json.loads(r.text)
    # print(dic)
    redis_store.set('access_token', dic['access_token'], ex=dic['expires_in'])
    redis_store.set('refresh_token', dic['refresh_token'], ex=dic['refresh_token_expires_in'])

    if r.status_code == 200:
        return json.dumps(return_success('ok'))
    else:
        return json.dumps(return_unsuccess('Failed to refresh'))


# 取消授权
@citi_api.route('/revokeAcc', methods=['POST', 'GET'])
def revokeAcc():
    url = 'https://sandbox.apihub.citi.com/gcb/api/authCode/oauth2/revoke'

    payload = "token={0}&token_type_hint={1}".format(redis_store.get('refresh_token'), 'refresh_token')

    headers = {
        'authorization': get_basic_auth(),
        'content-type': 'application/x-www-form-urlencoded',
        'accept': "application/json"
    }

    r = requests.post(url, data=payload, headers=headers)

    return r.text


# 获取卡的信息
@citi_api.route('/getCardsInfo', methods=["POST", "GET"])
def getCardsInfo():
    url = "https://sandbox.apihub.citi.com/gcb/api/v1/cards?cardFunction=ALL"
    # payload = "cardFunction=ALL"
    r = requests.get(url, headers=get_headers())
    # print(r.text)
    return r.text


# 获取账号信息
@citi_api.route('/getAccountsInfo', methods=["POST", "GET"])
def getAccountsInfo():
    url = "https://sandbox.apihub.citi.com/gcb/api/v1/accounts?nextStartIndex=1"

    r = requests.get(url, headers=get_headers())

    dic = json.loads(r.text)
    # print(dic)
    return r.text


# 获取客户信息
@citi_api.route('/getCustomerProfile', methods=["POST", "GET"])
def getCustomerProfile():
    url = "https://sandbox.apihub.citi.com/gcb/api/v1/customers/profiles"
    r = requests.get(url, headers=get_headers())
    dic = json.loads(r.text)
    # print(dic)
    return r.text


# 获取account详细信息
@citi_api.route('/getAccounts/<string:account_id>', methods=["POST", "GET"])
def getAccountById(account_id):
    url = "https://sandbox.apihub.citi.com/gcb/api/v1/accounts/" + account_id
    r = requests.get(url, headers=get_headers())
    dic = json.loads(r.text)
    # print(dic)
    return r.text


# 获取account交易信息
@citi_api.route('/getAccounts/transactions/<string:account_id>', methods=["POST", "GET"])
def getAccountTransactions(account_id):
    url = "https://sandbox.apihub.citi.com/gcb/api/v1/accounts/{0}/transactions".format(account_id)
    print(url)
    r = requests.get(url, headers=get_headers())
    dic = json.loads(r.text)
    # print(dic)
    return r.text
