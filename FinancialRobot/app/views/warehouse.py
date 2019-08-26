import uuid

from app.dao.GoodsDao import GoodsDao
from app.dao.WareHouseDao import WareHouseDao
from flask import Blueprint, render_template, request, session, jsonify
from app.utils.json_util import *

warehouse = Blueprint("warehouse", __name__)
warehouse.secret_key = 'secret_key_warehouse'


# 入库
@warehouse.route("/storeInWarehouse", methods=["POST"])
def store_in_warehouse():
    _json = request.json
    _companyId = _json.get("companyId")
    _id = _json.get("id")
    _wareHouseId = _json.get("wareHouseId")
    print(_json)
    warehouse_dao = WareHouseDao()
    try:
        warehouse_dao.storage(_companyId, _id, _wareHouseId)
        return jsonify(return_success(""))
    except Exception as e:
        return jsonify(return_unsuccess("添加失败" + str(e)))


# 查询库存
@warehouse.route("/queryStoreGoods", methods=["POST",'GET'])
def query_by_warehouse():
    _json = request.json
    _companyId = _json.get("companyId")
    _wareHouseId = _json.get("wareHouseId")
    _name = _json.get('name')
    _type = _json.get('type')
    print(_json)
    goods_dao = GoodsDao()
    res = goods_dao.query_by_warehouse(_companyId, _wareHouseId, _name, _type)
    size = len(res)
    if size >= 0:
        return json.dumps(return_success({'goodsList': GoodsDao.to_ware_dict(res)}),
                          cls=DecimalEncoder, ensure_ascii=False)
    else:
        return jsonify(return_unsuccess("查询失败"))


@warehouse.route('/deliverFromWareHouse', methods=['POST'])
def deliver_from_warehouse():
    _json = request.json
    _companyId = _json.get("companyId")
    _sellId = _json.get("sellId")
    _outList = _json.get("outList")
    res = WareHouseDao().out(_companyId, _sellId, _outList)
    if res:
        return json.dumps(return_success('Out success'))
    else:
        return json.dumps(return_unsuccess('Out Failed'))

# 添加仓库
@warehouse.route("/addWarehouse", methods=["POST"])
def addWarehouse():
    _json = request.json
    companyId = _json.get('companyId')
    name = _json.get('name')
    ID = str(uuid.uuid3(uuid.NAMESPACE_OID, name))
    site = _json.get('site')
    addWarehouse = WareHouseDao()
    row = addWarehouse.add(ID, name, site, companyId)
    if row == 1:
        return json.dumps(return_success(ID))
    else:
        return json.dumps(return_unsuccess('Error: Add failed'))


# 查询仓库
@warehouse.route("/queryWarehouse", methods=["POST"])
def queryWarehouse():
    _json = request.json
    companyId = _json.get('companyId')
    query = WareHouseDao()
    if _json.get('name') is None:
        Cusresult = query.query_byCompanyId(companyId)
        size = len(Cusresult)
        if size == 0:
            return json.dumps(return_unsuccess('Error: No data'))
        else:
            return json.dumps(return_success(WareHouseDao.to_dict(Cusresult)), ensure_ascii=False)
    else:
        name = _json.get('name')
        newname = '%' + name + '%'
        Cusresult = query.query_by_name(companyId, newname)
        size = len(Cusresult)
        if size == 0:
            return json.dumps(return_unsuccess('Error: No data'))
        else:
            return json.dumps(return_success(WareHouseDao.to_dict(Cusresult)), ensure_ascii=False)
