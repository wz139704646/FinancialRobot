#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from app.utils.DBHelper import MyHelper
import uuid
class PurchaseDao:
    @classmethod
    def to_dict(cls, data):
        result = []
        for row in data:
            res = {}
            res['goodId'] = row[0]
            res['supplierId'] = row[1]
            res['companyId'] = row[2]
            res['number'] = row[3]
            res['purchasePrice'] = row[4]
            res['date'] = row[5]
            result.append(res)
        return result
    def query_all(self):
        connection = MyHelper()
        return connection.executeQuery("select * from Purchase")
    def query_byCid(self,companyId):
        connection = MyHelper()
        return connection.executeQuery("select * from Purchase where companyId=%s",[companyId])
    def add(self, goodId, supplierId, companyId, number, purchasePrice,date):
        connection = MyHelper()
        row=connection.executeUpdate(
            "insert into Purchase (id, name, companyId, number, purchasePrice, date) VALUES (%s,%s,%s,%s,%s,%s)",
            [goodId, supplierId, companyId, number, purchasePrice, date])
        return row

