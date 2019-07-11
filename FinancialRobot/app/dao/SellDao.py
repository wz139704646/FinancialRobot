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

class SellDao:
    @classmethod
    def to_dict(cls, data):
        result = []
        for row in data:
            res = {}
            res['id'] = row[0]
            res['customerId'] = row[1]
            res['goodsId'] = row[2]
            res['companyId'] = row[3]
            res['number'] = row[4]
            res['sumprice'] = row[5]
            res['date'] = row[6]
            res['customerName'] = row[7]
            res['goodsName'] = row[8]
            result.append(res)
        return result
    def query_all(self):
        connection = MyHelper()
        return connection.executeQuery("select * from Sell")
    def query_byCid(self,companyId):
        connection = MyHelper()
        return connection.executeQuery("select * from Sell where companyId=%s",[companyId])
    def query_byDate(self, companyId,start,end):
        connection = MyHelper()
        return connection.executeQuery("select * from Sell where companyId=%s and date >= %s and date <%s", [companyId,start,end])
    def add(self,id,customerId, goodsId, companyId, number, sumprice,date,customerName,goodsName):
        connection = MyHelper()
        row=connection.executeUpdate(
            "insert into Sell (id,customerId, goodsId, companyId, number, sumprice,date,customerName,goodsName) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            [id,customerId, goodsId, companyId, number, sumprice,date,customerName,goodsName])
        return row
