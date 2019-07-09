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
            result.append(res)
        return result

    def query_all(self):
        connection = MyHelper()
        return connection.executeQuery("select * from Goods")

    def add(self, name, sellprice, companyId, type, unitInfo):
        id = uuid.uuid3(uuid.NAMESPACE_OID, str(time()))
        connection = MyHelper()
        row = connection.executeUpdate(
            "insert into Goods (id, name, sellprice, companyId, type, unitInfo) VALUES (%s,%s,%s,%s,%s,%s)",
            [str(id), name, sellprice, companyId, type, unitInfo])
        res={"row":row,"id":id.__str__()}
        return res

    def update_photo(self, id, photo):
        connection = MyHelper()
        row = connection.executeUpdate("update Goods set photo = %s where id = %s", [photo, id])
        return row

    def query_by_companyId(self, companyId, name, type):
        _param = [companyId]
        _sql = "select * from Goods where companyId = %s"
        if name:
            _sql += " and name like %s"
            _param.append('%' + name + '%')
        if type:
            _sql += " and type = %s"
            _param.append(type)
        connection = MyHelper()
        return connection.executeQuery(_sql, _param)
