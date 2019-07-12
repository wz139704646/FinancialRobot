#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import unittest
import requests
import uuid
import json
import jieba
import time,datetime
from flask import Blueprint, render_template, request
from app.dao.WareHouseDao import WareHouseDao
from app.dao.PurchaseDao import PurchaseDao,DecimalEncoder
from app.utils.DBHelper import MyHelper
from app.dao.CompanyDao import CompanyDao
from app.dao.SellDao import SellDao
from app.dao.CustomerDao import CustomerDao
from app.dao.SupplierDao import SupplierDao
from app.dao.GoodsDao import GoodsDao
from app.dao.UserDao import UserDao
from app.utils.res_json import *

# -*- encoding: utf-8 -*-

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
        supname = '街道口职业技术学院1'
        supcid = "1"
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
        print(json.dumps(return_success(CustomerDao.to_dict(supresult)),ensure_ascii = False))
class Test5(unittest.TestCase):
    def test5(self):
        queryAllsup = SupplierDao()
        supresult = queryAllsup.query_byCompanyId("1")
        size=len(supresult)
        print(supresult)
        supresu_json = json.dumps(SupplierDao.to_dict(supresult), ensure_ascii=False)
        print(size)
        print(supresu_json)
        print(json.dumps(return_success(SupplierDao.to_dict(supresult)), ensure_ascii=False))
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
class Test10(unittest.TestCase):
    def test10(self):
        KEYWORDS_URL = 'http://api.bosonnlp.com/keywords/analysis'
        text = '病毒式媒体网站：让新闻迅速蔓延'
        params = {'top_k': 10}
        data = json.dumps(text)
        headers = {
            'X-Token': 'w8HTxklZ.35565.o3kXzfrM77rR',
            'Content-Type': 'application/json'
        }
        resp = requests.post(KEYWORDS_URL, headers=headers, params=params, data=data.encode('utf-8'))
        for weight, word in resp.json():
            print(weight, word)
class Test11(unittest.TestCase):
    def test13(self):

        query = PurchaseDao()

        # size = len(result)
        # print(result)
        # purjson=json.dumps(PurchaseDao.to_dict(result), ensure_ascii=False,cls=DecimalEncoder)
        # print(purjson)
        # print(purjson)
        # companyId = "5"
        # goodsNo ="5dfac447-d039-3eae-bde9-33f832f17437"
        # number = 1
        # provideNo = "1"
        # purchasePrice = 10.5
        date = "2019-7-10"
        start = datetime.datetime.strptime(date, '%Y-%m-%d')
        delta = datetime.timedelta(days=1)
        n_days = start + delta
        end=n_days.strftime('%Y-%m-%d %H:%M:%S')
        print(start)
        print(n_days.strftime('%Y-%m-%d %H:%M:%S'))
        result = query.query_byDate("5",start,end)
        print(result)



        # row = query.add(goodsNo, provideNo, companyId, number, purchasePrice, date, "未入库")
        # if row == 1:
        #     return json.dumps(return_success("Yes!"))
        # else:
        #     return json.dumps(return_unsuccess('Error: Add failed'))
    def test11(self):
        addUser = UserDao()
        #row = addUser.add("123211","111","1","1")
        supresult = addUser.query_all()
        size=len(supresult)
        print(supresult)
        supresu_json = json.dumps(UserDao.to_dict(supresult), ensure_ascii=False)
        print(size)
        print(supresu_json)
        print(json.dumps(return_success(UserDao.to_dict(supresult)), ensure_ascii=False))
    def test13(self):
        queryCustomer = CustomerDao()
        result = queryCustomer.query_byId("031f50f8-7691-33b0-9281-cafeba075c90")
        print(len(result))
        print(result[0][1])
        print(result)
    def test14(self):
        query = SellDao()
        companyId ="5"
        date = "2019-7-11"
        if date == None:
            result = query.query_byCid(companyId)
            size = len(result)
            if size == 0:
                return json.dumps(return_unsuccess('Error: No data'))
            else:
                print(json.dumps(return_success(SellDao.to_dict(result)), ensure_ascii=False, cls=DecimalEncoder))
        else:
           # date = "2019-7-12"
            start = datetime.datetime.strptime(date, '%Y-%m-%d')
            delta = datetime.timedelta(days=1)
            n_days = start + delta
            end = n_days.strftime('%Y-%m-%d %H:%M:%S')
            result = query.query_byDate(companyId, start, end)
            size = len(result)
            if size == 0:
                return json.dumps(return_unsuccess('Error: No data'))
            else:
                print(json.dumps(return_success(SellDao.to_dict(result)), ensure_ascii=False, cls=DecimalEncoder))
    def test15(self):
        query = SellDao()
        queryCustomer = CustomerDao()
        queryGoods = GoodsDao()
        companyId ="5"
        customerId = "201353eb-4f3b-3992-bdae-347841dc304d"
        result = queryCustomer.query_byId(customerId)
        if len(result) == 1:
            customerName = result[0][1]
        else:
            customerName = ""
        sumprice = 22.5
        date = "2019-7-12"
        id = str(uuid.uuid3(uuid.NAMESPACE_OID, date))
        goodsId = "e7f00942-5aad-3df5-90d1-c850b0839ff2"
        number = 5
        goodsResult = queryGoods.query_byId(goodsId)
        if len(goodsResult) == 1:
            goodsName = goodsResult[0][1]
        else:
            goodsName = ""
        row = query.add(id, customerId, goodsId, companyId, number, sumprice, date, customerName, goodsName)
        if row == 1:
            return json.dumps(return_success("Yes!"))
        else:
            return json.dumps(return_unsuccess('Error: Add failed'))
    def test12(self):
        jieba.load_userdict("../app/utils/dict.txt")
        #去除停用词
        stopwords = {}.fromkeys(['的', '包括', '等', '是','多少'])
        time1 = ['今天', '这一天']
        time2 = ['昨天','上一天']
        time3 = ['这周','这一周']
        time4 = ['上周','上一周']
        time5 = ['这个月']

        action1 = ['赚', '挣', '卖', '收入', '盈利', '进账']
        action2 = ['进','买']
        action3 = ['查','看','查看']
        action4 = ['花', '消费', '支出']

        nouns1 = ['东西', '商品', '货']
        nouns2 = ['钱']
        nouns3 = ['库存']

        text1 = "上周进了多少货"
        text2 = "今天卖了多少东西"
        text3 = "看一下库存"
        text4 = "今天花了多少钱"
        # 精确模式
        segs = jieba.cut(text1, cut_all=False)
        final = []
        for seg in segs:
            if seg not in stopwords:
                final.append(seg)
        print(final)
        time = 1
        for item in final:
            if time == 1:
                if item in time2:
                    time = 2
                if item in time3:
                    time = 3
                if item in time4:
                    time = 4
                if item in time5:
                    time = 5
            if item in action1:
                action = 1
            if item in action2:
                action = 2
            if item in action3:
                action = 3
            if item in action4:
                action = 4
            if item in nouns1:
                nouns = 1
            if item in nouns2:
                nouns = 2
            if item in nouns3:
                nouns = 3
        print(time)
        print(action)
        print(nouns)
        if action==1 and nouns==1:
            if time == 1:
                print("今天的销售量")
            if time ==2:
                print("昨天的销售量")
            if time ==3:
                print("这周的销售量")
            if time ==4:
                print("上周的销售量")
            if time ==5:
                print("这个月的销售量")
        if action ==1 and nouns ==2:
            if time == 1:
                print("今天的销售额")
            if time == 2:
                print("昨天的销售额")
            if time == 3:
                print("这周的销售额")
            if time == 4:
                print("上周的销售额")
            if time == 5:
                print("这个月的销售额")
        if action ==2 and nouns ==1:
            if time == 1:
                print("今天进的货")
            if time == 2:
                print("昨天的进的货")
            if time == 3:
                print("这周进的货")
            if time == 4:
                print("上周进的货")
            if time == 5:
                print("这个月进的货")
        if action == 3 and (nouns == 1 or nouns ==3):
            if time == 1:
                print("今天的库存")
            if time == 2:
                print("今天的库存")
            if time == 3:
                print("今天的库存")
            if time == 4:
                print("今天的库存")
            if time == 5:
                print("今天的库存")
        if action == 4 and nouns == 2 :
            if time == 1:
                print("今天花了多少钱")
            if time == 2:
                print("昨天花了多少钱")
            if time == 3:
                print("这周花了多少钱")
            if time == 4:
                print("上周花了多少钱")
            if time == 5:
                print("这个月花了多少钱")



