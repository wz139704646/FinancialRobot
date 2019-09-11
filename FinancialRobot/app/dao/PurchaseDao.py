#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from app.utils.DBHelper import MyHelper
import uuid
import decimal, json
import datetime


# class DecimalEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, decimal.Decimal):
#             return float(o)
#         if isinstance(o, datetime.datetime):
#             return o.strftime("%Y-%m-%d %H:%M:%S")
#         else:
#             super(DecimalEncoder, self).default(o)

class PurchaseDao:
    @classmethod
    def to_dict(cls, data):
        result = []
        for row in data:
            res = {}
            res['id'] = row[0]
            res['status'] = row[1]
            res['supplierId'] = row[2]
            res['date'] = row[3]
            res['supplierName'] = row[4]
            goodslist = []
            for good in row[5]:
                goods = {}
                goods['price'] = good[0]
                goods['goodsId'] = good[1]
                goods['goodsPhoto'] = good[2]
                goods['goodsName'] = good[3]
                goods['number'] = good[4]
                goodslist.append(goods)
            res['goodsList'] = goodslist
            result.append(res)
        return result

    def query_all(self):
        connection = MyHelper()
        return connection.executeQuery("select * from Purchase")

    def query_byDate(self, companyId, start, end):
        connection = MyHelper()
        return connection.executeQuery(
            "select distinct id ,date from Purchase where companyId=%s and date >= %s and date <%s order by date ",
            [companyId, start, end])

    def query_byCid(self, companyId):
        connection = MyHelper()
        return connection.executeQuery("select * from Purchase where companyId=%s", [companyId])

    def query_byId(self, id):
        connection = MyHelper()
        return connection.executeQuery("select * from Purchase where id = %s", [id])

    def query_ForPic(self, start, end):
        connection = MyHelper()
        return connection.executeQuery(
            "select SUM(number*purchasePrice),date from Purchase where date >= %s and date <%s group by date ",
            [start, end])

    def purchasePriceByName(self, name):
        connection = MyHelper()
        return connection.executeQuery(
            "SELECT DISTINCT(purchasePrice), date ,goodName,supplierId FROM Purchase WHERE goodName LIKE %s ORDER BY date", [name])

    def queryAllId(self, companyId):
        connection = MyHelper()
        return connection.executeQuery("select distinct id ,date from Purchase where companyId = %s order by date ",
                                       [companyId])

    def add(self, id, goodId, goodName, supplierId, companyId, number, purchasePrice, date, status):
        connection = MyHelper()
        row = connection.executeUpdate(
            "insert into Purchase (id,goodId, goodName, supplierId, companyId, number, purchasePrice, date,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            [id, goodId, goodName, supplierId, companyId, number, purchasePrice, date, status])
        return row
