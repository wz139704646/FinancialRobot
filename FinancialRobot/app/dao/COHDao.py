#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from app.utils.DBHelper import MyHelper

class COHDao:
    @classmethod
    def to_dict(cls, data):
        result = []
        for row in data:
            res = {}
            res['id'] = row[0]
            res['date'] = row[1]
            res['balance'] = row[2]
            res['originValue'] = row[3]
            res['variation'] = row[4]
            res['changeDescription'] = row[5]
            result.append(res)
        return result
    def queryNow(self):
        conn = MyHelper()
        return conn.executeQuery("select * from CashOnHand order by date desc ")
    def queryAll(self):
        conn = MyHelper()
        return conn.executeQuery("select * from CashOnHand order by date")

    def query_by_date(self,start,end):
        connection = MyHelper()
        return connection.executeQuery("select * from CashOnHand where date >= %s and date <%s",
                                       [start, end])
    def add(self, id, date, balance,originValue,variation,changeDescription):
        conn = MyHelper()
        row = conn.executeUpdate("insert into CashOnHand (id, date, balance,originValue,variation,changeDescription) VALUES (%s,%s,%s,%s,%s,%s)" ,[id, date, balance,originValue,variation,changeDescription])
        return row