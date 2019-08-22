#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from app.utils.DBHelper import MyHelper


class WareHouseDao:
    @classmethod
    def to_dict(cls, data):
        result = []
        for row in data:
            res = {}
            res['id'] = row[0]
            res['name'] = row[1]
            res['site'] = row[2]
            res['companyId'] = row[3]
            result.append(res)
        return result

    def queryAllInfo(self):
        connection = MyHelper()
        return connection.executeQuery("select * from Warehouse")

    def query_byCompanyId(self, cid):
        connection = MyHelper()
        return connection.executeQuery("select * from Warehouse where companyId = %s", [cid])

    def query_by_name(self, companyId, name):
        conn = MyHelper()
        return conn.executeQuery("select * from Warehouse where companyId = %s and name like %s", [companyId, name])

    def add(self, id, name, site, companyId):
        connection = MyHelper()
        row = connection.executeUpdate('insert into Warehouse(id, \
        name, site,companyId) \
         values (%s,%s,%s,%s)', [id, name, site, companyId])
        return row

    def storage(self, companyId, purchaseId, wareHouseId):
        connection = MyHelper()
        try:
            in_goods = connection.executeQuery("select * from Purchase where companyId = %s and id = %s",
                                               [companyId, purchaseId])
            connection.executeUpdate("update Purchase set status = '到' where companyId = %s and id = %s",
                                     [companyId, purchaseId])
            for in_good in in_goods:
                connection.executeUpdate(
                    "insert into GoodsStore (goodsId, wareId, companyId, number) VALUES (%s,%s,%s,%s) "
                    "on duplicate key update "
                    "number = number + %s",
                    [in_good[1], wareHouseId, companyId, in_good[5], in_goods[5]])
            return True
        except Exception as e:
            print(e)
            return False

    # 入库
    def out(self, company_id, sell_id, out_list):
        connection = MyHelper()
        _sql = []
        _params = []
        for goods in out_list:
            goods_id = goods.get('goodsId')
            warehouse_id = goods.get('wareHouseId')
            number = goods.get('number')
            _sql.append('update GoodsStore set number = number - %s where companyId = %s '
                        'and wareId = %s and goodsId=%s')
            _params.append([number, company_id, warehouse_id, goods_id])
        _sql.append('update Sell set status = 1 where id = %s')
        _params.append([sell_id])
        return connection.executeUpdateTransaction(_sql, params=_params)
