#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import unittest
import requests
import time
import os
import urllib.request
from bs4 import BeautifulSoup
import re
import uuid
import json
import jieba
import string
import flask
import datetime
from flask import Blueprint, render_template, request
from app.dao.WareHouseDao import WareHouseDao
from app.dao.COHDao import COHDao
from app.dao.PurchaseDao import PurchaseDao
from app.dao.BankStatementDao import BankStatementDao
from app.utils.DBHelper import MyHelper
from app.utils.timeProcess import timeProcess
from app.dao.CompanyDao import CompanyDao
from app.dao.DailyfundDao import DailyfundDao
from app.dao.SellDao import SellDao
from app.dao.CustomerDao import CustomerDao
from app.dao.SupplierDao import SupplierDao
from app.dao.GoodsDao import GoodsDao

from app.utils.json_util import *


# -*- encoding: utf-8 -*-

class Test1(unittest.TestCase):
    def test1(self):
        date = datetime.datetime.now()
        print(date)


class Test2(unittest.TestCase):
    def test2(self):
        query = CompanyDao()
        result = query.queryAll()
        result_json = json.dumps(CompanyDao.to_dict(result), ensure_ascii=False)
        print(result)
        print(result_json)


class Test3(unittest.TestCase):
    def test3(self):
        supquery = SupplierDao()
        supname = '街道口职业技术学院1'
        supcid = "1"
        supid = str(uuid.uuid3(uuid.NAMESPACE_OID, supname))
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
        print(json.dumps(return_success(CustomerDao.to_dict(supresult)), ensure_ascii=False))


class Test5(unittest.TestCase):
    def test5(self):
        queryAllsup = SupplierDao()
        supresult = queryAllsup.query_byCompanyId("1")
        size = len(supresult)
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
        bankname = "珞珈山银行"
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
        print(supresu_json)


class Test8(unittest.TestCase):
    def test8(self):
        conn = MyHelper()
        name = "嘉"
        companyId = "5"
        input = '%' + name + '%'
        # and name like / % " + name + " / % "
        result = conn.executeQuery("select * from Customer where companyId = %s and name LIKE %s ", [companyId, input])
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
        end = n_days.strftime('%Y-%m-%d %H:%M:%S')
        print(start)
        print(n_days.strftime('%Y-%m-%d %H:%M:%S'))
        result = query.query_byDate("5", start, end)
        print(result)

        # row = query.add(goodsNo, provideNo, companyId, number, purchasePrice, date, "未入库")
        # if row == 1:
        #     return json.dumps(return_success("Yes!"))
        # else:
        #     return json.dumps(return_unsuccess('Error: Add failed'))

    # def test11(self):
    #     addUser = UserDao()
    #     # row = addUser.add("123211","111","1","1")
    #     supresult = addUser.query_all()
    #     size = len(supresult)
    #     print(supresult)
    #     supresu_json = json.dumps(UserDao.to_dict(supresult), ensure_ascii=False)
    #     print(size)
    #     print(supresu_json)
    #     print(json.dumps(return_success(UserDao.to_dict(supresult)), ensure_ascii=False))

    def test13(self):
        queryCustomer = CustomerDao()
        result = queryCustomer.query_byId("031f50f8-7691-33b0-9281-cafeba075c90")
        print(len(result))
        print(result[0][1])
        print(result)

    def test14(self):
        query = SellDao()
        companyId = "5"
        date = "2019-7-11"
        if date == None:
            result = query.query_byCid(companyId)
            size = len(result)
            if size == 0:
                return json.dumps(return_unsuccess('Error: No data'))
            else:
                print(json.dumps(return_success(SellDao.to_dict(result)), ensure_ascii=False))
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
                print(json.dumps(return_success(SellDao.to_dict(result)), ensure_ascii=False))

    def test15(self):
        query = SellDao()
        queryCustomer = CustomerDao()
        queryGoods = GoodsDao()
        companyId = "5"
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

    def test16(self):
        date = "2019-7-12"
        start = datetime.datetime.strptime(date, '%Y-%m-%d')
        monday = timeProcess.get_current_week(start)
        print(monday)
        delta = datetime.timedelta(days=7)
        n_days = monday + delta
        print(n_days)
        fist = datetime.date(start.year, start.month - 1, 1)
        last = datetime.date(start.year, start.month, 1) - datetime.timedelta(1)
        print(fist)
        print(last)

    def test17(self):
        query = PurchaseDao()
        date = "2019-7-10"
        inputTime = datetime.datetime.strptime(date, '%Y-%m-%d')
        delta = datetime.timedelta(days=1)
        n_days = inputTime + delta
        end = n_days.strftime('%Y-%m-%d %H:%M:%S')
        start = inputTime
        result = query.query_byDate("5", start, end)
        finalresult = []
        print(result[0])
        outMoneyarray = []
        outMoney = 0
        for buy in result:
            mid = "购入 " + buy[2] + " " + str(buy[5]) + "个" + "，单价" + str(buy[6]) + "元"
            outMoney += float(buy[4]) * float(buy[5])
            finalresult.append(mid)
        outString = "进货支出" + str(outMoney) + "元"
        outMoneyarray.append(outString)
        print(outMoneyarray)
        print(finalresult)

    def test20(self):
        id = str(uuid.uuid3(uuid.NAMESPACE_OID, "1"))
        id2 = str(uuid.uuid3(uuid.NAMESPACE_OID, "1"))
        print(id)
        print(id2)

    def test21(self):
        ad = BankStatementDao()
        result = ad.queryByName('花旗银行')
        a = len(result)
        print(a)
        print(result[0][7])

    def test22(self):
        a = "2019-07-24 19:11:03"
        d = datetime.datetime.strptime(a, '%Y-%m-%d %H:%M:%S')
        b = "2019-07-25 19:11:03"
        db = datetime.datetime.strptime(b, '%Y-%m-%d %H:%M:%S')
        date_zero = d.replace(year=d.year, month=d.month, day=d.day, hour=0, minute=0, second=0)
        date_tomorrow = d.replace(year=d.year, month=d.month, day=d.day + 1, hour=0, minute=0, second=0)
        if db >= date_zero and db < date_tomorrow:
            print("I love you")
        dateZero = date_zero.strftime('%Y-%m-%d %H:%M:%S')
        print(dateZero)
        print(date_tomorrow.strftime('%Y-%m-%d %H:%M:%S'))

    def test23(self):
        query = SellDao()
        result = query.queryGoodsAllInfo('d6c4af7e-786a-3ce2-891c-96d8d031f579')
        print(result)

    def test24(self):
        data = {"companyId": "5",
                "name": "zqr", }
        token = request.headers.get('Authorization')
        _resp = requests.post(url='http://127.0.0.1:5000/queryCustomerByName', json=data, headers=request.headers)
        resp_json = _resp.content
        print(resp_json)

    def test25(self):
        query = SellDao()
        results = []
        idresult = query.queryAllId()
        print(idresult)
        print(len(idresult))
        if len(idresult) != 0:
            for j in range(0, len(idresult)):
                result = []
                id = idresult[j][0]
                customerName = ""
                customerId = ""
                date = ""
                goodslist = []
                goodsResult = query.query_byId(id)
                for i in range(0, len(goodsResult)):
                    customerName = goodsResult[i][7]
                    customerId = goodsResult[i][1]
                    date = goodsResult[i][6]
                    goods = []
                    goods.append(goodsResult[i][2])
                    goods.append(goodsResult[i][5])
                    goods.append(goodsResult[i][4])
                    goods.append(goodsResult[i][8])
                    goodslist.append(goods)
                result.append(id)
                result.append(customerId)
                result.append(customerName)
                result.append(date)
                result.append(goodslist)
                results.append(result)
        print(results)
        print(len(results))

    def test35(self):
        query = SupplierDao()
        result = query.query_byId('08580344-22e0-34a6-9cce-774279c9b9a8')
        print(result[0][1])

    def test26(self):
        query = PurchaseDao()
        results = []
        idResult = query.queryAllId("5")
        size = len(idResult)
        if size == 0:
            return json.dumps(return_unsuccess('Error: No data'))
        else:
            for j in range(0, len(idResult)):
                result = []
                id = idResult[j][0]
                goodsList = []
                goodsResult = query.query_byId(id)
                for i in range(0, len(goodsResult)):
                    status = goodsResult[i][8]
                    supplierId = goodsResult[i][3]
                    date = goodsResult[i][7]
                    goods = []
                    goods.append(goodsResult[i][6])
                    goods.append(goodsResult[i][1])
                    goods.append(goodsResult[i][2])
                    goods.append(goodsResult[i][5])
                    goodsList.append(goods)
                result.append(id)
                result.append(status)
                result.append(supplierId)
                result.append(date)
                result.append(goodsList)
                results.append(result)
        print(results)

    def test30(self):
        companyId = "5"
        date = "2019-7-14"
        language = ""
        jieba.load_userdict("../app/utils/dict.txt")
        # 去除停用词
        stopwords = {}.fromkeys(['的', '包括', '等', '是', '多少', "所有", "一下"])
        today = ['今天', '这一天']
        yesterday = ['昨天', '上一天']
        this_week = ['这周', '这一周']
        last_week = ['上周', '上一周']
        this_month = ['这个月']

        ac_in_money = ['赚', '挣', '卖', '收入', '盈利', '进账']
        ac_purchase = ['进', '买']
        ac_query = ['查', '看', '查看', "查询"]
        ac_out_money = ['花', '消费', '支出']

        goods = ['东西', '商品', '货', "货物"]
        money = ['钱']
        store = ['库存']

        text1 = "上周进了多少货"
        text2 = "今天卖了什么东西"
        text3 = "查询商品可口可乐的库存"
        text5 = "查一下所有商品的库存"
        text4 = "今天花了多少钱"
        # 精确模式
        segs = jieba.cut(text3, cut_all=False)
        final = []
        for seg in segs:
            if seg not in stopwords:
                final.append(seg)
        print(final)
        a = 0
        for i in range(0, len(final)):
            if final[i] == "库存":
                a = i - 1
        print(final[a])

    def test31(self):
        a=0
        for i in range(1,5):
            a=a+i
        print(a)
        basedir = os.path.abspath(os.path.dirname('sell.py'))
        print(basedir)
        result = []
        nowTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        #nowTime=time.localtime(time.time())
        print(nowTime)
        # query = SellDao()
        # result = query.query_byId("96277eb0-79a8-36b9-9b4a-f95d7b6055d0")
        # print(result)
    def test32(self):
        url = r'http://www.whalebj.com/xzjc/default.aspx'
        html = urllib.request.urlopen(url).read().decode('utf-8')

        soup = BeautifulSoup(html,features='lxml')

        temp = soup.find_all(
            'span'
        )[0]

        temp = str(temp)
        time = re.findall(r'\d+-\d+-\d+ \d+:\d+:\d+', temp)

        daiyun_car = re.findall(r'待运车辆数为：\d+', temp)

        jinchang_car = re.findall(r'进场车辆数为：\d+', temp)

        lichang_car = re.findall(r'离场车辆数为：\d+', temp)

        print(time[0], daiyun_car[0][7:], jinchang_car[0][7:], lichang_car[0][7:])
    def test36(self):
        query = COHDao()
        result = query.query_by_date('2019-10-01 00:00:00', '2019-11-01 00:00:00')
        print(result)
    def test37(self):
        query=SellDao()
        InfoResult=query.queryGoodsIdByPage(20,0);
        print(InfoResult)

    def test12(self):

        companyId = "5"
        date1 = "2019-07-24 19:11:03"
        date = "2019-07-24"
        d = datetime.datetime.strptime(date1, '%Y-%m-%d %H:%M:%S')
        language = ""
        jieba.load_userdict("../app/utils/dict.txt")
        # 去除停用词
        stopwords = {}.fromkeys(['的', '包括', '等', '是', '多少', "所有", "一下"])
        today = ['今天', '这一天']
        yesterday = ['昨天', '上一天']
        this_week = ['这周', '这一周']
        last_week = ['上周', '上一周']
        this_month = ['这个月']

        ac_in_money = ['赚', '挣', '卖', '收入', '盈利', '进账']
        ac_purchase = ['进', '买', "进了", "买了"]
        ac_query = ['查', '看', '查看', "查询"]
        ac_out_money = ['花', '消费', '支出']

        goods = ['东西', '商品', '货', "货物"]
        money = ['钱']
        price = ['价格']
        inPrice = ['进价']
        outPrice = ['售价']
        store = ['库存']
        supplier = ['供货商', '供应商', '进货商']
        customer = ['顾客', '客户']
        tables = ['利润表', '资产负债表', '经营日报', '利润分析']

        text1 = "这个月卖了什么货"
        text2 = "这个月挣了多少钱"
        text3 = "查一下商品可口可乐的售价"
        text4 = "这个月挣了多少钱"
        # 精确模式
        segs = jieba.cut(text3, cut_all=False)
        final = []
        for seg in segs:
            if seg not in stopwords:
                final.append(seg)
        print(final)
        time = "today"
        for item in final:
            if time == "today":
                if item in yesterday:
                    time = "yesterday"
                if item in this_week:
                    time = "this_week"
                if item in last_week:
                    time = "last_week"
                if item in this_month:
                    time = "this_month"
            if item in ac_in_money:
                action = "ac_in_money"
            if item in ac_purchase:
                action = "ac_purchase"
            if item in ac_query:
                action = "ac_query"
            if item in ac_out_money:
                action = "ac_out_money"
            if item in goods:
                nouns = "goods"
            if item in money:
                nouns = "money"
            if item in store:
                nouns = "store"
            if item in price:
                nouns = "price"
            if item in inPrice:
                nouns = "inPrice"
            if item in outPrice:
                nouns = "outPrice"
            if item in supplier:
                nouns = "supplier"
            if item in customer:
                nouns = "customer"
            if item in tables:
                nouns = "tables"
        print(time)
        print(action)
        print(nouns)

        querySell = SellDao()
        queryPurchase = PurchaseDao()
        inputTime = datetime.datetime.strptime(date, '%Y-%m-%d')
        # 对时间进行判断
        if time == "today":
            start = d.replace(year=d.year, month=d.month, day=d.day, hour=0, minute=0, second=0)
            end = d.replace(year=d.year, month=d.month, day=d.day + 1, hour=0, minute=0, second=0)
        if time == "yesterday":
            start = d.replace(year=d.year, month=d.month, day=d.day - 1, hour=0, minute=0, second=0)
            end = d.replace(year=d.year, month=d.month, day=d.day, hour=0, minute=0, second=0)
        if time == "this_week":
            newDay = d.replace(year=d.year, month=d.month, day=d.day, hour=0, minute=0, second=0)
            start = timeProcess.get_current_week(newDay)
            delta = datetime.timedelta(days=7)
            end = start + delta
        if time == "last_week":
            end = timeProcess.get_current_week(d)
            delta = datetime.timedelta(days=7)
            start = end - delta
        if time == "this_month":
            start = d.replace(year=d.year, month=d.month, day=1, hour=0, minute=0, second=0)
            end = d.replace(year=d.year, month=d.month + 1, day=1, hour=0, minute=0, second=0)
        print(time)
        print(start)
        print(end)
        # token = request.headers.get('Authorization')
        token = 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzI5NTkyOTgsImlhdCI6MTU2Nzc3NTI5OCwiZGF0YSI6eyJhY2NvdW50IjoiMTU4MjcxNTI2NzAiLCJsb2dpbl90aW1lIjoxNTY3Nzc1Mjk4fX0.UqCe-5K99K_HPL8UglxtYUHNLpj_f7rWC3M39SjNRfw'
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        # 对行为进行判断
        ##### 一段时期内的销售情况 #####
        if action == "ac_in_money" and nouns == "goods":
            data = {"start": start,
                    "end": end,
                    'companyId': '5',
                    'date': "hh"}
            data_json = json.dumps(data, cls=DecimalEncoder)
            sellRecords = requests.post(url='http://127.0.0.1:5000/querySell', data=data_json, headers=headers)
            SellResult = json.loads(sellRecords.content)
            if SellResult['success'] == True:
                sellResult = SellResult['result']
                print(sellResult)
                groups = []
                goodsType=[]
                group = {}
                activeNames = []
                items = []
                for sellRecord in sellResult:
                    item = {}
                    goodsList = sellRecord['goodsList']
                    lists = []
                    content = {}
                    for goods in goodsList:
                        goodsId = goods['goodsId']
                        queryGoodsType = GoodsDao()
                        goodType = queryGoodsType.queryType_byId(goodsId)
                        if goodType[0][0] not in goodsType:
                            goodsType.append(goodType[0][0])
                        list = {}
                        list['title'] = goods['goodsName']
                        list['value'] = goods['number']
                        list['label'] = goods['goodsId']
                        lists.append(list)
                    content['type'] = 'list'
                    content['lists'] = lists
                    item['title'] = sellRecord['date']
                    item['value'] = '顾客' + sellRecord['customerName']
                    item['label'] = sellRecord['id']
                    item['content'] = content
                    items.append(item)
                group['activeNames'] = activeNames
                group['items'] = items
                groups.append(group)
                sellInfo = {'type': 'collapse-group',
                            'summary': '该段时间的销售信息如下：',
                            'groups': groups}
                print(json.dumps(sellInfo))
                return json.dumps(sellInfo)
        ##### 某段时间内进的货物 #####
        if action == "ac_purchase" and nouns == "goods":
            data = {'companyId': '5',
                    'date': "hh",
                    'start': start,
                    'end': end}
            data_json = json.dumps(data, cls=DecimalEncoder)
            if time=='this_month':
                queryForPic=PurchaseDao()
                PicResult= queryForPic.query_ForPic(start,end)
                datas = {}
                datas['type'] = 'line_chart',
                for picData in PicResult:
                    datas[picData[1]] = picData[0]
                print(datas)
            purchaseRecords = requests.post(url='http://127.0.0.1:5000/queryPurchase', data=data_json, headers=headers)
            SellResult = json.loads(purchaseRecords.content)
            print(SellResult)
            if SellResult['success'] == True:
                sellResult = SellResult['result']
                goodsType = []
                print(sellResult)
                groups = []
                group = {}
                activeNames = []
                items = []
                for sellRecord in sellResult:
                    item = {}
                    goodsList = sellRecord['goodsList']
                    lists = []
                    content = {}
                    for goods in goodsList:
                        goodsId = goods['goodsId']
                        queryGoodsType = GoodsDao()
                        goodType = queryGoodsType.queryType_byId(goodsId)
                        if goodType[0][0] not in goodsType:
                            goodsType.append(goodType[0][0])
                        list = {}
                        list['title'] = goods['goodsName']
                        list['value'] = goods['number']

                        list['label'] = goods['goodsId']
                        lists.append(list)
                    content['type'] = 'list'
                    content['lists'] = lists
                    item['title'] = sellRecord['date']
                    item['value'] = '供货商' + sellRecord['supplierName']
                    item['label'] = sellRecord['id']
                    item['content'] = content
                    items.append(item)
                group['activeNames'] = activeNames
                group['items'] = items
                groups.append(group)
                sellInfo = {'type': 'collapse-group',
                            'summary': '该段时间的进货信息如下：',
                            'groups': groups}
                print(json.dumps(sellInfo))

                sumPriceByType = []
                sumNumByType=[]
                for gType in goodsType:
                    sumOneType = 0
                    sumOneNum=0
                    for sellRecord in sellResult:
                        goodsList = sellRecord['goodsList']
                        for goods in goodsList:
                            goodsId = goods['goodsId']
                            queryGoodsType = GoodsDao()
                            goodType = queryGoodsType.queryType_byId(goodsId)
                            if goodType[0][0] == gType:
                                sumOneType = sumOneType+goods['number'] * goods['price']
                                sumOneNum = sumOneNum + goods['number']
                    sumPriceByType.append(sumOneType)
                    sumNumByType.append(sumOneNum)
                print(goodsType)
                print(sumPriceByType)
                print(sumNumByType)
                return json.dumps(sellInfo)
        ###### 查商品库存#####
        if action == "ac_query" and (nouns == "goods" or nouns == "store"):
            queryWare = WareHouseDao()
            Cusresult = queryWare.query_byCompanyId('5')
            print(Cusresult)
            if len(final) == 3:
                if final[1] in goods:
                    groups = []
                    activeNames = []
                    group = {}
                    items = []
                    for cusresult in Cusresult:
                        item = {}
                        content = {}
                        data = {'companyId': '5',
                                'wareHouseId': cusresult[0]}
                        data_json = json.dumps(data, cls=DecimalEncoder)
                        goodsStore = requests.post(url='http://127.0.0.1:5000/queryStoreGoods', data=data_json,
                                                   headers=headers)
                        Goodsstore = json.loads(goodsStore.content)
                        if Goodsstore['success'] == True:
                            goodsResult = Goodsstore['result']
                            goodsList = goodsResult['goodsList']
                            lists = []
                            for goods in goodsList:
                                list = {}
                                list['title'] = goods['name']
                                list['value'] = str(goods['amount']) + goods['unitInfo']
                                list['label'] = goods['id']
                                lists.append(list)
                        content['type'] = 'list'
                        content[lists] = lists
                        item['content'] = content
                        item['title'] = cusresult[1]
                        item['value'] = cusresult[2]
                        items.append(item)
                    group['items'] = items
                    group['activeNames'] = activeNames
                    groups.append(group)
                    print(groups)
                    storeInfo = {'type': 'collapse-group',
                                 'summary': '所有仓库的库存信息如下：',
                                 'groups': groups}
                    print(json.dumps(storeInfo))
                    return json.dumps(storeInfo)
                else:
                    data = {'companyId': '5',
                            'name': final[1]}
                    data_json = json.dumps(data, cls=DecimalEncoder)
                    goodsStore = requests.post(url='http://127.0.0.1:5000/queryStoreGoods', data=data_json,
                                               headers=headers)
                    Goodsstore = json.loads(goodsStore.content)
                    if Goodsstore['success'] == True:
                        goodsRecords = Goodsstore['result']
                        queryGoodsResult = goodsRecords['goodsList']
                        print(queryGoodsResult)
                        summary = ""
                        for goodResult in queryGoodsResult:
                            summary = summary + "商品" + goodResult['name'] + "当前库存为：" + str(int(goodResult['amount'])) + \
                                      goodResult['unitInfo'] + '\n'
                        print(summary)
                        storeInfo = {'type': 'text',
                                     'summary': summary}
                        return json.dumps(storeInfo)
                    else:
                        return None
            else:
                data = {'companyId': '5',
                        'name': final[2]}
                data_json = json.dumps(data, cls=DecimalEncoder)
                goodsStore = requests.post(url='http://127.0.0.1:5000/queryStoreGoods', data=data_json, headers=headers)
                Goodsstore = json.loads(goodsStore.content)
                if Goodsstore['success'] == True:
                    goodsRecords = Goodsstore['result']
                    queryGoodsResult = goodsRecords['goodsList']
                    print(queryGoodsResult)
                    summary = ""
                    for goodResult in queryGoodsResult:
                        summary = summary + "商品" + goodResult['name'] + "当前库存为：" + str(int(goodResult['amount'])) + \
                                  goodResult['unitInfo'] + '\n'
                    print(summary)
                    storeInfo = {'type': 'text',
                                 'summary': summary}
                    return json.dumps(storeInfo)
                else:
                    return None
        # 查询商品的价格
        if action == "ac_query" and (nouns == "price" or nouns == "inPrice" or nouns == "outPrice"):
            if len(final) == 3:
                data = {'name': final[1]}
            else:
                data = {'name': final[2]}
            data_json = json.dumps(data, cls=DecimalEncoder)
            judge = 0
            allgroups = []
            averageInmoney = 0
            NewInmoney = 0
            averageOutmoney = 0
            NewOutmoney = 0
            if nouns == "price":
                judge = 1
            if nouns == "inPrice" or judge == 1:
                _respIn = requests.post(url='http://127.0.0.1:5000/purchasePriceByName', data=data_json,
                                        headers=headers)
                inRecords = json.loads(_respIn.content)
                if inRecords['success'] == True:
                    inRecord = inRecords['result']
                    groups = []
                    group = {}
                    items = []
                    count = 0
                    sumPrice = 0
                    newPrice = 0
                    for inGoods in inRecord:
                        item = {}
                        item['title'] = inGoods['goodName']
                        item['value'] = inGoods['purchasePrice']
                        sumPrice = sumPrice + inGoods['purchasePrice']
                        NewInmoney = newPrice = inGoods['purchasePrice']
                        count = count + 1
                        querySupName = SupplierDao()
                        supID = inGoods['supplierId']
                        querySupNameResult = querySupName.queryName_byId(supID)
                        print(querySupNameResult[0][0])
                        item['label'] = '供货商：' + querySupNameResult[0][0]
                        item['tag'] = inGoods['date']
                        items.append(item)
                    group['title'] = '商品的进价情况如下'
                    group['items'] = items
                    allgroups.append(group)
                    groups.append(group)
                    averageInmoney = round(sumPrice / count, 2)
                    Price = {'type': 'list-group',
                             'summary': '商品最新进价为' + str(newPrice) + "元，平均进价为" + str(round(sumPrice / count, 2)) + "元",
                             'groups': groups}
            if nouns == "outPrice" or judge == 1:
                _respOut = requests.post(url='http://127.0.0.1:5000/SellPriceByName', data=data_json, headers=headers)
                inRecords = json.loads(_respOut.content)
                if inRecords['success'] == True:
                    inRecord = inRecords['result']
                    print(inRecord)
                    groups = []
                    group = {}
                    items = []
                    count = 0
                    sumPrice = 0
                    newPrice = 0
                    for inGoods in inRecord:
                        item = {}
                        item['title'] = inGoods['goodsName']
                        item['value'] = str(round(inGoods['sumprice'] / inGoods['number'], 2)) + "元"
                        sumPrice = sumPrice + inGoods['sumprice'] / inGoods['number']
                        NewOutmoney = newPrice = inGoods['sumprice'] / inGoods['number']
                        count = count + 1
                        item['label'] = '客户：' + inGoods['customerName']
                        item['tag'] = inGoods['date']
                        items.append(item)
                    group['title'] = '商品的售价情况如下'
                    group['items'] = items
                    groups.append(group)
                    allgroups.append(group)
                    averageOutmoney = round(sumPrice / count, 2)
                    Price = {'type': 'list-group',
                             'summary': '商品最新售价为' + str(newPrice) + "元，平均售价为" + str(round(sumPrice / count, 2)) + "元",
                             'groups': groups}
            if nouns == "price":
                Price = {'type': 'list-group',
                         'summary': '商品最新售价为' + str(NewOutmoney) + "元，平均售价为" + str(
                             averageOutmoney) + "元 " + ' 商品最新进价为' + str(NewInmoney) + "元，平均进价为" + str(
                             averageInmoney) + "元",
                         'groups': allgroups}
            print(Price)
            return json.dumps(Price)

        #### 一段时间的收入或支出####
        if nouns == "money":
            data = {'start': start,
                    'end': end}
            data_json = json.dumps(data, cls=DecimalEncoder)
            _respCash = requests.post(url='http://127.0.0.1:5000/queryCashRecordByDate', data=data_json,
                                      headers=headers)
            CashResult = json.loads(_respCash.content)
            inCash = outCash = 0
            if CashResult['success'] == True:
                cashResult = CashResult['result']
                for sinCash in cashResult:
                    if sinCash['variation'] > 0:
                        inCash = inCash + sinCash['variation']
                    else:
                        outCash = outCash + sinCash['variation']
            _respBank = requests.post(url='http://127.0.0.1:5000/queryBankRecordByDate', data=data_json,
                                      headers=headers)
            inBank = outBank = 0
            BankResult = json.loads(_respBank.content)
            if BankResult['success'] == True:
                bankResult = BankResult['result']
                for sinBank in bankResult:
                    if sinBank['amount'] > 0:
                        inBank = inBank + sinBank['amount']
                    else:
                        outBank = outBank + sinBank['amount']
            if action == "ac_in_money":
                summary = '现金收入' + str(inCash) + '元，银行存款、转账等收入' + str(inBank) + '元，共计' + str(inBank + inCash) + '元'
                inMoney = {'type': 'text',
                           'summary': summary}
                return json.dumps(inMoney)
            if action == "ac_out_money":
                outBank = abs(outBank)
                outCash = abs(outCash)
                summary = '现金支出' + str(outCash) + '元，银行存款、转账等支出' + str(outBank) + '元，共计' + str(outCash + outCash) + '元'
                outMoney = {'type': 'text',
                            'summary': summary}
                return json.dumps(outMoney)
        #####查询顾客信息#####
        if action == "ac_query" and nouns == "customer":
            name = ''
            print(final[3])
            for i in range(2, len(final) - 1):
                if final[i] != '信息':
                    name = name + final[i]
            print(name)
            data = {'companyId': '5',
                    'name': name}
            data_json = json.dumps(data, cls=DecimalEncoder)
            _respCustomer = requests.post(url='http://127.0.0.1:5000/queryCustomer', data=data_json, headers=headers)
            CustomerDaoResult = json.loads(_respCustomer.content)
            if CustomerDaoResult['success'] == True:
                customerResult = CustomerDaoResult['result']
                groups = []
                for supplier in customerResult:
                    group = {}
                    items = []
                    for key in supplier:
                        res = {}
                        res['title'] = key
                        res['value'] = supplier[key]
                        items.append(res)
                    group['items'] = items
                    groups.append(group)
                print(groups)
                supplierInfo = {'type': 'list-group',
                                'summary': '客户' + name + '的信息',
                                'groups': groups}
                return json.dumps(supplierInfo)
            else:
                return None
            CusResult = _respCash.content
            customerInfo = {'type': 'list-group',
                            'summary': '客户' + name + '的信息'}
            print(CusResult)
        #####查询供应商信息#####
        if action == "ac_query" and nouns == "supplier":
            name = ''
            for i in range(2, len(final) - 1):
                if final[i] != '信息':
                    name = name + final[i]
            print(name)
            data = {'companyId': '5',
                    'name': name}
            data_json = json.dumps(data, cls=DecimalEncoder)
            _respSupplier = requests.post(url='http://127.0.0.1:5000/querySupplierByName', data=data_json,
                                          headers=headers)
            SupplierResult = json.loads(_respSupplier.content)
            if SupplierResult['success'] == True:
                supplierResult = SupplierResult['result']
                groups = []
                for supplier in supplierResult:
                    group = {}
                    items = []
                    for key in supplier:
                        res = {}
                        res['title'] = key
                        res['value'] = supplier[key]
                        items.append(res)
                    group['items'] = items
                    groups.append(group)
                print(groups)
                supplierInfo = {'type': 'list-group',
                                'summary': '供应商' + name + '的信息',
                                'groups': groups}
                return json.dumps(supplierInfo)
            else:
                return None
        #####查询表格信息#####
        if action == "ac_query" and nouns == "tables":
            data = {'start': start,
                    'end': end}
            data_json = json.dumps(data, cls=DecimalEncoder)
            _respCash = requests.post(url='http://127.0.0.1:5000/queryCashRecordByDate', data=data_json,
                                      headers=headers)
            CashResult = _respCash.content
            print(CashResult)
