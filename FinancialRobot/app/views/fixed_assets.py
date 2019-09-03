from flask import Flask, request, redirect, Blueprint
import requests
from app.utils.auth import *

fixed_assets = Blueprint("fixed_assets", __name__)
fixed_assets.secret_key = 'fixed_assetsxxxx'

fixed_assets_uri = 'https://www.fibot.cn/django'


@fixed_assets.before_request
@check_token
def res():
    pass


@fixed_assets.route('/FixedAssets', methods=['GET'])
def query_fixed_assets():
    url = fixed_assets_uri + '/fixed_asset/'
    res = requests.get(url, params=request.args)
    return res.content


@fixed_assets.route('/FixedAssets', methods=['POST'])
def add_fixed_assets():
    url = fixed_assets_uri + '/fixed_asset/'
    res = requests.post(url, json=request.json)
    return res.content


@fixed_assets.route('/FixedAssets/<string:asset_id>', methods=['PUT'])
def dep_fixed_assets(asset_id):
    url = fixed_assets_uri + '/fixed_asset/' + asset_id
    res = requests.put(url, data=request.json)
    return res.content
