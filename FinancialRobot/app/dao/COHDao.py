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
            res['variation'] = row[2]
            res['changeDescription'] = row[3]
            result.append(res)
        return result

    def queryNow(self):
        conn = MyHelper()
        return conn.executeQuery("select * from CashOnHand order by date desc ")

    def queryAll(self):
        conn = MyHelper()
        return conn.executeQuery("select * from CashOnHand order by date")

    def query_by_date(self, start, end):
        connection = MyHelper()
        return connection.executeQuery("select * from CashOnHand where date >= %s and date <%s order by date ",
                                       [start, end])

    def add(self, id, date, variation, changeDescription):
        conn = MyHelper()
        row = conn.executeUpdate(
            "insert into CashOnHand (id, date,variation,changeDescription) VALUES (%s,%s,%s,%s)",
            [id, date,  variation, changeDescription])
        return row
