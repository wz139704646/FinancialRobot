#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from app.utils.DBHelper import MyHelper


class DailyfundDao:
    @classmethod
    def to_dict(cls, data):
        result = []
        for row in data:
            res = {}
            res['yesterMoney'] = row[0]
            res['changeExplain'] = row[1]
            res['nowMoney'] = row[2]
            res['changeAmount'] = row[3]
            res['date'] = row[4]
            result.append(res)
        return result

    def InsertToday(self, changeExplain, nowMoney, changeAmount, date):
        conn = MyHelper()
        row = conn.executeUpdate("update Dailyfund set changeExplain=%s,nowMoney=%s,changeAmount=%s where date =%s",
                                 [changeExplain, nowMoney, changeAmount, date])
        return row

    def queryAll(self):
        conn = MyHelper()
        return conn.executeQuery("select * from Dailyfund order by date desc ")

    def queryAllDaily(self):
        conn = MyHelper()
        return conn.executeQuery("select * from Dailyfund order by date ")

    def query_by_date(self, date):
        connection = MyHelper()
        return connection.executeQuery("select * from Dailyfund where date = %s", [date])

    def query_by_SD(self, start, end):
        connection = MyHelper()
        return connection.executeQuery("select * from Dailyfund where date >= %s and date <%s order by date ",
                                       [start, end])

    def add(self, yesterMoney, changeExplain, nowMoney, changeAmount, date):
        conn = MyHelper()
        row = conn.executeUpdate(
            "insert into Dailyfund (yesterMoney, changeExplain, nowMoney,changeAmount,date) VALUES (%s,%s,%s,%s,%s)",
            [yesterMoney, changeExplain, nowMoney, changeAmount, date])
        return row
