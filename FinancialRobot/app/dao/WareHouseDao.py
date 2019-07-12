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
    def add(self,id, name, site, companyId):
        connection = MyHelper()
        row = connection.executeUpdate('insert into Warehouse(id, \
        name, site,companyId) \
         values (%s,%s,%s,%s)', [id, name,site, companyId])
        return row

