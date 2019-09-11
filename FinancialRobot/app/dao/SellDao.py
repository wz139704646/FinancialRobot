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

class SellDao:
    @classmethod
    def to_dict(cls, data):
        result = []
        for row in data:
            res = {}
            res['id'] = row[0]
            res['customerId'] = row[1]
            res['customerName'] = row[2]
            res['date'] = row[3]
            res['status'] = row[5]
            goodslist=[]
            for good in row[4]:
                goods = {}
                goods['goodsId'] = good[0]
                goods['sumprice'] = good[1]
                goods['price'] = good[1]
                goods['number'] = good[2]
                goods['goodsName'] = good[3]
                goods['goodsPhoto'] = good[4]
                goodslist.append(goods)
            res['goodsList'] =goodslist
            result.append(res)
        return result

    def query_all(self):
        connection = MyHelper()
        return connection.executeQuery("select * from Sell order by date desc")

    def queryAllId(self):
        conn = MyHelper()
        return conn.executeQuery("select distinct (id),date from Sell ORDER BY date")

    def queryGoodsInfo(self,id):
        conn=MyHelper()
        return conn.executeQuery("select sumprice,goodsId,number,goodsName from Sell where id=%s",[id])

    def query_byId(self, id):
        connection = MyHelper()
        return connection.executeQuery("select * from Sell where id = %s", [id])

    def query_byCid(self, companyId):
        connection = MyHelper()
        return connection.executeQuery("select * from Sell where companyId=%s  order by date desc", [companyId])

    def query_byDate(self, companyId, start, end):
        connection = MyHelper()
        return connection.executeQuery("select distinct (id),date from Sell where companyId=%s and date >= %s and date <%s  order by date desc",
                                       [companyId, start, end])

    def add(self, id, customerId, goodsId, companyId, number, sumprice, date, customerName, goodsName, unitInfo):
        connection = MyHelper()
        row = connection.executeUpdate(
            "insert into Sell (id,customerId, goodsId, companyId, number, sumprice,date,customerName,goodsName,unitInfo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            [id, customerId, goodsId, companyId, number, sumprice, date, customerName, goodsName, unitInfo])
        return row

    def query_ForPic(self, start, end):
        connection = MyHelper()
        return connection.executeQuery(
            "select SUM(sumPrice),date from Sell where date >= %s and date <%s group by date ",
            [start, end])
    def SellPriceByName(self, name):
        connection = MyHelper()
        return connection.executeQuery(
            "SELECT number ,sumprice, date,goodsName,customerName FROM Sell WHERE goodsName LIKE %s ORDER BY date", [name])
