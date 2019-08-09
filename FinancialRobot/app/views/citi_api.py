import base64
import http.client
import uuid

from flask import Blueprint, render_template, request, session, jsonify, redirect
import requests
from urllib import parse
import json
from app.config import redis_store

citi_api = Blueprint("citi_api", __name__)
citi_api.secret_key = 'secret_key_citi_api'

CLIENT_ID = "31b2b8c1-8449-4828-8147-c98799373f2d"
CLIENT_SECRET = "C7jW0pM0tJ5cF7eO0gR6gT7cO8wY2jI5sG8qL0iW7hC4cK4lM3"
SCOPE = "accounts_details_transactions customers_profiles payees personal_domestic_transfers " \
        "internal_domestic_transfers external_domestic_transfers bill_payments cards onboarding reference_data "
STATE = "12321"
REDIRECT_URI = "http://127.0.0.1:5000/getAccToken"
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


def get_authorization():
    secret = CLIENT_ID + ":" + CLIENT_SECRET
    b64secret = base64.b64encode(secret.encode())
    return 'Basic ' + b64secret.decode()


def get_token_auth(acc_token):
    return "Bearer " + acc_token


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
        'countryCode': 'US',
        'businessCode': 'GCB',
        'locale': 'en_US',
        'state': STATE,
        'redirect_uri': REDIRECT_URI
    }
    # r = requests.get(url=url, params=parameters, headers=headers)
    auth = get_url(url, parameters)
    return redirect(auth)


@citi_api.route("/oauth/redirect", methods=["POST", "GET"])
def oauth():
    code = request.args.get('code')
    state = request.args.get('state')
    if code and state == STATE:
        print(code)
        return "<h1>Authorization code grant success !!</h1>"
    else:
        return "<h1>Authorization code grant failed !!</h1>"


@citi_api.route("/getAccToken", methods=["POST", "GET"])
def getAccToken():
    code = request.args.get('code')
    state = request.args.get('state')
    if not (code and state == STATE):
        return "<h1>Authorization code grant failed !!</h1>"
    url = "https://sandbox.apihub.citi.com/gcb/api/authCode/oauth2/token/hk/gcb"

    payload = "grant_type=authorization_code&code={0}&redirect_uri={1}".format(code, REDIRECT_URI)

    headers = {
        'authorization': get_authorization(),
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept': "application/json"
    }

    r = requests.post(url, data=payload, headers=headers)
    # print(r.text)
    # print(r.status_code)
    dic = json.loads(r.text)
    print(dic)
    # redis_store.set()
    access_token = dic['access_token']
    print(access_token)
    refresh_token = dic['refresh_token']
    getAccountsInfo(access_token)
    return redirect(INDEX)


@citi_api.route('/getCardsInfo', methods=["POST", "GET"])
def getCardsInfo(access_token=None):
    url = "https://sandbox.apihub.citi.com/gcb/api/v1/cards"
    if not access_token:
        access_token = redis_store.get('account')

    payload = "cardFunction=ALL"
    headers = {
        'Authorization': get_token_auth(access_token),
        'client_id': CLIENT_ID,
        'uuid': str(uuid.uuid4()),
        'Accept': "application/json",
        'Content-Type': "application/json"
    }
    r = requests.get(url, data=payload, headers=headers)
    print(r.text)
    return r.text


@citi_api.route('/getAccountsInfo', methods=["POST", "GET"])
def getAccountsInfo(access_token=None):
    url = "https://sandbox.apihub.citi.com/gcb/api/v1/accounts"
    if not access_token:
        access_token = request.json.get('access_token')
        # access_token = redis_store.get('account')

    headers = {
        'Authorization': get_token_auth(access_token),
        'client_id': CLIENT_ID,
        'uuid': str(uuid.uuid4()),
        'Accept': "application/json",
        'content-type': 'application/json'
    }
    # r = requests.get(url, headers=headers)
    conn = http.client.HTTPSConnection("sandbox.apihub.citi.com")
    conn.request("GET", "/gcb/api/v1/accounts", headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))
    # print(r.text)
    return data
