#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from app.utils.DBHelper import MyHelper


class SupplierDao:
    @classmethod
    def to_dict(cls, data):
        result = []
        for row in data:
            res = {}
            res['id'] = row[0]
            res['name'] = row[1]
            res['phone'] = row[2]
            res['site'] = row[3]
            res['taxpayerNumber'] = row[4]
            res['bankaccount'] = row[5]
            res['bankname'] = row[6]
            res['companyId'] = row[7]
            result.append(res)
        return result

    def queryAll(self):
        conn = MyHelper()
        return conn.executeQuery("select * from Supplier")

    def query_byCompanyId(self, companyId):
        conn = MyHelper()
        return conn.executeQuery("select * from Supplier where companyId = %s", [companyId])

    def query_byId(self, id):
        connection = MyHelper()
        return connection.executeQuery("select * from Supplier where id = %s", [id])

    def queryName_byId(self, id):
        connection = MyHelper()
        return connection.executeQuery("select name from Supplier where id = %s", [id])

    def query_byName(self, name):
        connection = MyHelper()
        return connection.executeQuery("select * from Supplier where name like %s", [name])

    def add(self, id, name, phone, site, taxpayerNumber, bankaccount, bankname, companyId):
        conn = MyHelper()
        row = conn.executeUpdate(
            "insert into Supplier (id, name, phone,site,taxpayerNumber,bankaccount,bankname,companyId) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
            [id, name, phone, site, taxpayerNumber, bankaccount, bankname, companyId])
        return row
