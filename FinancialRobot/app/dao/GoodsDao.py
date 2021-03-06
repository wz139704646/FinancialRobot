from app.utils.DBHelper import MyHelper
import uuid
from time import time


class GoodsDao:
    @classmethod
    def to_dict(cls, data):
        result = []
        for row in data:
            res = {}
            res['id'] = row[0]
            res['name'] = row[1]
            res['sellprice'] = row[2]
            res['companyId'] = row[3]
            res['type'] = row[4]
            res['unitInfo'] = row[5]
            res['brand'] = row[6]
            res['photo'] = row[7]
            res['barcode'] = row[8]
            res['WarehouseId'] = row[9]
            result.append(res)
        return result

    def query_all(self):
        connection = MyHelper()
        return connection.executeQuery("select * from Goods")

    def query_byId(self, id):
        conn = MyHelper()
        return conn.executeQuery("select * from Goods where id = %s", [id])

    def queryType_byId(self, id):
        conn = MyHelper()
        return conn.executeQuery("select type from Goods where id = %s", [id])

    def add(self, name, sellprice, companyId, type, unitInfo, barcode):
        id = uuid.uuid3(uuid.NAMESPACE_OID, str(time()))
        connection = MyHelper()
        row = connection.executeUpdate(
            "insert into Goods (id, name, sellprice, companyId, type, unitInfo,barcode) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            [str(id), name, sellprice, companyId, type, unitInfo, barcode])
        res = {"row": row, "id": id.__str__()}
        return res

    def update_photo(self, _id, photo):
        connection = MyHelper()
        row = connection.executeUpdate("update Goods set photo = %s where id = %s", [photo, _id])
        return row

    def update_info(self, _id, name, sellprice, _type, unitInfo, barcode):
        connection = MyHelper()
        row = connection.executeUpdate("update Goods set name = %s, sellprice=%s,type=%s,unitInfo=%s,barcode=%s "
                                       "where id = %s", [name, sellprice, _type, unitInfo, barcode, _id])
        return row

    @classmethod
    def get_BuyPrice(self, id):
        connection = MyHelper()
        row = connection.executeQuery("select purchasePrice from Purchase where goodId = %s", [id])
        return row[0][0]

    def query_by_companyId(self, companyId, name, type,id):
        _param = [companyId]
        _sql = "select * from Goods where companyId = %s"
        if id:
            _sql += " and id=  %s"
            _param.append(id)
        if name:
            _sql += " and name like %s"
            _param.append('%' + name + '%')
        if type:
            _sql += " and type = %s"
            _param.append(type)
        connection = MyHelper()
        return connection.executeQuery(_sql, _param)

    @classmethod
    def to_ware_dict(cls, data):
        result = []
        for row in data:
            res = {}
            res['id'] = row[0]
            res['name'] = row[1]
            res['type'] = row[2]
            res['sellprice'] = row[3]
            res['unitInfo'] = row[4]
            res['amount'] = row[5]
            res['photo'] = row[6]
            result.append(res)
        return result

    # 根据仓库查库存
    def query_by_warehouse(self, companyId, wareHouseId=None, name=None, _type=None):
        connection = MyHelper()
        _sql = "select Goods.id, Goods.name, Goods.type, Goods.sellprice," \
               "Goods.unitInfo,sum(GoodsStore.number), Goods.photo " \
               "from Goods, GoodsStore " \
               "where Goods.id=GoodsStore.goodsId and Goods.companyId = %s"
        _param = [companyId]
        if name:
            _sql += " and Goods.name like %s"
            _param.append('%' + name + '%')
        if _type:
            _sql += " and Goods.type like %s"
            _param.append('%' + _type + '%')
        if wareHouseId:
            _sql += " and GoodsStore.wareId = %s"
            _param.append(wareHouseId)

        _sql += " group by Goods.id"
        return connection.executeQuery(_sql, _param)

    @classmethod
    def to_ware_goods_amount_dict(cls, data):
        result = []
        for row in data:
            res = {'wareHouseId': row[0], 'wareHouseName': row[1], 'number': row[2]}
            result.append(res)
        return result

    # 根据商品号查库存
    def query_store_by_goods_id(self, company_id, goods_id):
        connection = MyHelper()
        _sql = "select GoodsStore.wareId,Warehouse.name, GoodsStore.number from GoodsStore,Warehouse" \
               " where Warehouse.id=GoodsStore.wareId and goodsId = %s and %s in " \
               "(select GoodsStore.goodsId from GoodsStore where GoodsStore.companyId = %s) " \
               "and  GoodsStore.companyId = %s"
        _param = [goods_id, goods_id, company_id, company_id]
        return connection.executeQuery(_sql, _param)
