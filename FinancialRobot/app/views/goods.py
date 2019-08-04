from flask import Blueprint, render_template, request, session, jsonify
from app.utils.json_util import *
from app.dao.GoodsDao import GoodsDao

goods = Blueprint("goods", __name__)
goods.secret_key = 'secret_key_goods'

# 添加商品
@goods.route("/addGoods", methods=['POST'])
def addGoods():
    _json = request.json
    print(_json)
    goods_dao = GoodsDao()
    res = goods_dao.add(_json.get('name'), _json.get('sellprice'), _json.get('companyId'),
                        _json.get('type'), _json.get('unitInfo'))
    if res["row"] == 1:
        return json.dumps(return_success({"id": res["id"]}))
    else:
        return json.dumps(return_unsuccess("添加商品失败"), ensure_ascii=False)

# 查询商品
@goods.route("/queryGoods", methods=['POST'])
def queryGoods():
    _json = request.json
    companyId = _json.get('companyId')
    name = _json.get('name')
    type = _json.get('type')
    goods_dao = GoodsDao()
    result = goods_dao.query_by_companyId(companyId, name, type)
    size = len(result)
    if size >= 0:
        return json.dumps(return_success({'goodsList': GoodsDao.to_dict(result)}),
                          cls=DecimalEncoder, ensure_ascii=False)
    else:
        return json.dumps(return_unsuccess("查询失败"), ensure_ascii=False)
