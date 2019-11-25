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
            res['sumCount'] = row[4]
            res['status'] = row[6]
            goodslist = []
            for good in row[5]:
                goods = {}
                goods['goodsId'] = good[0]
                goods['sumprice'] = decimal.Decimal(good[1]).quantize(decimal.Decimal("0.00"))
                goods['price'] = decimal.Decimal(good[1]).quantize(decimal.Decimal("0.00"))
                goods['number'] = good[2]
                goods['goodsName'] = good[3]
                goods['goodsPhoto'] = good[4]
                goodslist.append(goods)
            res['goodsList'] = goodslist
            result.append(res)
        return result

    def query_all(self):
        connection = MyHelper()
        return connection.executeQuery("select * from Sell order by date desc")

    def queryAllId(self):
        conn = MyHelper()
        return conn.executeQuery("select distinct (id),date from Sell ORDER BY date")

    def queryIdByName(self,name,limit,offset):
        conn = MyHelper()
        return conn.executeQuery("select distinct id from Sell where customerName like %s limit %s offset %s",[name,limit,offset])
    def queryGoodsInfo(self, id):
        conn = MyHelper()
        return conn.executeQuery("select sumprice,goodsId,number,goodsName from Sell where id=%s", [id])

    def query_byId(self, id):
        connection = MyHelper()
        return connection.executeQuery("select * from Sell where id = %s", [id])

    def queryGoodsAllInfo(self,id):
        connection = MyHelper()
        return connection.executeQuery("select * from Goods,Sell where Sell.id=%s and Sell.goodsId=Goods.id ",[id])

    def queryGoodsIdByPage(self, limit, offset):
        connection = MyHelper()
        return connection.executeQuery("select distinct id,date from Sell order by date desc limit %s offset %s",[limit,offset])
        #return connection.executeQuery("select distinct id,date from Sell order by date")

    def query_byCid(self, companyId):
        connection = MyHelper()
        return connection.executeQuery("select * from Sell where companyId=%s  order by date desc", [companyId])

    def query_byDate(self, companyId, start, end,limit,offset):
        connection = MyHelper()
        return connection.executeQuery(
            "select distinct (id),date from Sell where companyId=%s and date >= %s and date <%s  order by date desc limit %s offset %s",
            [companyId, start, end,limit,offset])

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
            "SELECT number ,sumprice, date,goodsName,customerName FROM Sell WHERE goodsName LIKE %s ORDER BY date",
            [name])

    def sellRecommendList(self):
        connection = MyHelper()
        return connection.executeQuery(
            """select customerId,goodsId,min(t) as T from  (
                SELECT a.customerId,a.customerName,a.goodsId,a.goodsName,TIMESTAMPDIFF(DAY,b.date,a.date) as t
                From Sell as a left join Sell as b on a.customerId = b.customerId
                where  DATE (a.date) > DATE(b.date) AND a.goodsName = b.goodsName
                ) as Temp
            group by customerId,goodsId
            """
        )

    def sellRecommendByUserGoods(self,uid,gid):
        connection = MyHelper()
        return connection.executeQuery("""
            select  customerId,customerName,goodsId,goodsName,date from Sell 
            where customerId = %s and goodsId = %s order by date desc limit 1
        """,[uid,gid])

    def sellRecommendUser(self):
        connection = MyHelper()
        return connection.executeQuery(
            """select customerId,goodsId,min(t) as T from  (
                SELECT a.customerId,a.customerName,a.goodsId,a.goodsName,TIMESTAMPDIFF(DAY,b.date,a.date) as t
                From Sell as a left join Sell as b on a.customerId = b.customerId
                where  DATE (a.date) > DATE(b.date) AND a.goodsName = b.goodsName
                ) as Temp
            group by customerId,goodsId
            """
        )
