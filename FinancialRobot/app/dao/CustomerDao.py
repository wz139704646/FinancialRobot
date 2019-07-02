#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from app.utils.DBHelper import MyHelper

class CustomerDao:
    @classmethod
    def to_dict(cls, data):
        result = []
        for row in data:
            res = {}
            res['id'] = row[0]
            res['name'] = row[1]
            res['phone'] = row[2]
            res['credit'] = row[3]
            res['companyId'] = row[4]
            res['bankName'] = row[5]
            res['bankAccount'] = row[6]
            result.append(res)
        return result
    def queryAll(self):
        conn = MyHelper()
        return conn.executeQuery("select * from Customer")
    def query_by_name(self,companyId,name):
        conn = MyHelper()
        return conn.executeQuery("select * from Customer where companyId = %s and name like %s", [companyId,name])
    def query_by_phone(self,companyId,phone):
        conn = MyHelper()
        return conn.executeQuery("select * from Customer where companyId = %s and phone like %s", [companyId,phone])
    def query_byCompanyId(self,companyId):
        conn = MyHelper()
        return conn.executeQuery("select * from Customer where companyId = %s",[companyId])
    def add(self, id, name, phone,credit,companyId,bankName,bankAccount):
        conn = MyHelper()
        row = conn.executeUpdate("insert into Customer (ID, name, phone,credit,companyId,bankName,bankAccount) VALUES (%s,%s,%s,%s,%s,%s,%s)" ,[id, name, phone,credit,companyId,bankName,bankAccount])
        return  row