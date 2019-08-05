#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from app.utils.DBHelper import MyHelper


class BankStatementDao:
    @classmethod
    def to_dict(cls, data):
        result = []
        for row in data:
            res = {}
            res['voucher'] = row[0]
            res['bankName'] = row[1]
            res['companyName'] = row[2]
            res['clearForm'] = row[3]
            res['amount'] = row[4]
            res['date'] = row[5]
            res['status'] = row[6]
            res['balance'] = row[7]
            res['sumBalance'] = row[8]
            result.append(res)
        return result

    def queryByName(self, bankName):
        conn = MyHelper()
        return conn.executeQuery("select * from BankStatement where bankName = %s order by date desc ", [bankName])

    def queryNow(self):
        conn = MyHelper()
        return conn.executeQuery("select * from BankStatement order by date desc ")

    def queryAll(self):
        conn = MyHelper()
        return conn.executeQuery("select * from BankStatement order by date")

    def query_by_date(self, start, end):
        connection = MyHelper()
        return connection.executeQuery("select * from BankStatement where date >= %s and date <%s",
                                       [start, end])

    def add(self, voucher, bankName, companyName, clearForm, amount, date, status, balance, sumBalance):
        conn = MyHelper()
        row = conn.executeUpdate(
            "insert into BankStatement (voucher, bankName, companyName,clearForm,amount,date,status,balance,sumBalance) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            [voucher, bankName, companyName, clearForm, amount, date, status, balance, sumBalance])
        return row
