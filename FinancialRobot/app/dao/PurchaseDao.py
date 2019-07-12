#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from app.utils.DBHelper import MyHelper
import uuid
import  decimal,json
import datetime
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        else:
            super(DecimalEncoder, self).default(o)

class PurchaseDao:
    @classmethod
    def to_dict(cls, data):
        result = []
        for row in data:
            res = {}
            res['id']=row[0]
            res['goodId'] = row[1]
            res['goodName'] = row[2]
            res['supplierId'] = row[3]
            res['companyId'] = row[4]
            res['number'] = row[5]
            res['purchasePrice'] = row[6]
            res['date'] = row[7]
            res['status'] = row[8]
            result.append(res)
        return result
    def query_all(self):
        connection = MyHelper()
        return connection.executeQuery("select * from Purchase")
    def query_byCid(self,companyId):
        connection = MyHelper()
        return connection.executeQuery("select * from Purchase where companyId=%s",[companyId])
    def query_byId(self, id):
        connection = MyHelper()
        return connection.executeQuery("select * from Purchase where id = %s", [id])
    def add(self, id, goodId, goodName, supplierId, companyId, number, purchasePrice,date,status):
        connection = MyHelper()
        row=connection.executeUpdate(
            "insert into Purchase (id,goodId, goodName, supplierId, companyId, number, purchasePrice, date,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            [id,goodId, goodName, supplierId, companyId, number, purchasePrice, date,status])
        return row


