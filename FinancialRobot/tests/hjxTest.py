#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import unittest
import json
from app.dao.WareHouseDao import WareHouseDao
from app.utils.DBHelper import MyHelper
from flask import Blueprint, render_template, request
from app.dao.CompanyDao import CompanyDao
from app.dao.CustomerDao import CustomerDao
from app.dao.SupplierDao import SupplierDao
from app.utils.res_json import *
import uuid
import json

class Test1(unittest.TestCase):
    def test1(self):
        a=WareHouseDao()
        result = a.getAllInfo()
        print(result)

class Test2(unittest.TestCase):
    def test2(self):
        query = CompanyDao()
        result = query.queryAll()
        result_json = json.dumps(CompanyDao.to_dict(result),ensure_ascii=False)
        print(result)
        print(result_json)

class Test3(unittest.TestCase):
    def test3(self):
        supquery = SupplierDao()
        supname = '街道口职业技术学院'
        supcid = "5"
        supid = str(uuid.uuid3(uuid.NAMESPACE_OID,supname))
        supphone = "12306"
        site = "信村"
        taxpayerNumber = "4000"
        bankname = "花旗银行"
        bankaccount = "1125"
        supquery.add(supid, supname, supphone, site, taxpayerNumber, bankaccount, bankname, supcid)
class Test4(unittest.TestCase):
    def test4(self):
        queryAllsup = CustomerDao()
        supresult = queryAllsup.queryAll()


       # print(json.dumps(return_success({'customerList': CustomerDao.to_dict(supresult)}),
                        #    ensure_ascii=False))
        print(json.dumps(return_success(CustomerDao.to_dict(supresult)),ensure_ascii = False))
       # supresu_json = json.dumps(CustomerDao.to_dict(supresult), ensure_ascii=False)
        #print(supresu_json)

     #   print(json.dumps(return_success(supresu_json)))
class Test5(unittest.TestCase):
    def test5(self):
        queryAllsup = SupplierDao()
        supresult = queryAllsup.query_byCompanyId("2")
        size=len(supresult)
        print(supresult)
        supresu_json = json.dumps(SupplierDao.to_dict(supresult), ensure_ascii=False)
        print(size)
        print(supresu_json)
class Test6(unittest.TestCase):
    def test6(self):
        companyId = "4"
        name = "张嘉吉"
        ID = str(uuid.uuid3(uuid.NAMESPACE_OID, name))
        phone = "173"
        bankAccount = "411"
        bankname ="珞珈山银行"
        credit = "优秀"
        addCustomer = CustomerDao()
        row = addCustomer.add(ID, name, phone, credit, companyId, bankname, bankAccount)
        print(row)
class Test7(unittest.TestCase):
    def test7(self):
        queryAllsup = CustomerDao()
        supresult = queryAllsup.query_byCompanyId("5")
        size = len(supresult)
        print(supresult)
        supresu_json = json.dumps(CustomerDao.to_dict(supresult), ensure_ascii=False)
        id = supresu_json['id']

        print(id)
        print(supresu_json)
class Test8(unittest.TestCase):
    def test8(self):
        conn = MyHelper()
        name="嘉"
        companyId="5"
        input = '%'+name+'%'
        #and name like / % " + name + " / % "
        result= conn.executeQuery("select * from Customer where companyId = %s and name LIKE %s ",[companyId,input])
        size = len(result)
        print(size)
        print(result)
class Test9(unittest.TestCase):
    def test9(self):
        jsonranklist = [{"xlid": "cxh", "xldigitid": 123456, "topscore": 2000, "topplaytime": "2009-08-20"},
                        {"xlid": "zd", "xldigitid": 123456, "topscore": 1500, "topplaytime": "2009-11-20"}];

        name = jsonranklist['xlid']
        phone = jsonranklist['xldigitid']
        print(name)
        print(phone)