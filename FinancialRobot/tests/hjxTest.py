#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import unittest
import requests
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
        result = query.query_all()
        print(result)

    def test24(self):
        data = {"companyId": "5",
                "name": "zqr", }
        _resp = requests.post(url='http://127.0.0.1:5000/queryCustomerByName', json=data)
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
        query = BankStatementDao()
        result = query.querySumAmount()
        print(result[0][0])
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
        stopwords = {}.fromkeys(['的', '包括', '等', '是', '多少', "所有"])
        today = ['今天', '这一天']
        time2 = ['昨天', '上一天']
        time3 = ['这周', '这一周']
        time4 = ['上周', '上一周']
        time5 = ['这个月']

        action1 = ['赚', '挣', '卖', '收入', '盈利', '进账']
        action2 = ['进', '买']
        action3 = ['查', '看', '查看']
        action4 = ['花', '消费', '支出']

        nouns1 = ['东西', '商品', '货']
        nouns2 = ['钱']
        nouns3 = ['库存']

        text1 = "上周进了多少货"
        text2 = "今天卖了什么东西"
        text3 = "查询可口可乐的库存"
        text5 = "查一下商品库存"
        text4 = "今天花了多少钱"
        # 精确模式
        segs = jieba.cut(text5, cut_all=False)
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
        query=SellDao()
        result=query.query_byId("96277eb0-79a8-36b9-9b4a-f95d7b6055d0")
        print(result)

    def test12(self):
        companyId = "5"
        date = "2019-7-14"
        language = ""
        jieba.load_userdict("../app/utils/dict.txt")
        # 去除停用词
        stopwords = {}.fromkeys(['的', '包括', '等', '是', '多少', "所有","一下"])
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
        text3 = "查一下可口可乐的库存"
        text4 = "今天花了多少钱"
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
        print(time)
        print(action)
        print(nouns)
        querySell = SellDao()
        queryPurchase = PurchaseDao()
        inputTime = datetime.datetime.strptime(date, '%Y-%m-%d')
        # 对时间进行判断
        if time == "today":
            delta = datetime.timedelta(days=1)
            n_days = inputTime + delta
            end = n_days.strftime('%Y-%m-%d %H:%M:%S')
            start = inputTime
        if time == "yesterday":
            delta = datetime.timedelta(days=1)
            n_days = inputTime - delta
            start = n_days.strftime('%Y-%m-%d %H:%M:%S')
            end = inputTime
        if time == "this_week":
            start = timeProcess.get_current_week(inputTime)
            delta = datetime.timedelta(days=7)
            end = start + delta
        if time == "last_week":
            end = timeProcess.get_current_week(inputTime)
            delta = datetime.timedelta(days=7)
            start = end - delta
        if time == "this_month":
            start = datetime.date(inputTime.year, inputTime.month - 1, 1)
            end = datetime.date(inputTime.year, inputTime.month, 1) - datetime.timedelta(1)
        print(start)
        print(end)
        # 对行为进行判断
        if action == "ac_in_money":
            resultInfo = []
            resultString = ""
            inMoney = 0
            outMoney = 0
            result = querySell.query_byDate(companyId, start, end)
            size = len(result)
            if size >= 1:
                for i in result:
                    purchasePrice = GoodsDao.get_BuyPrice(i[2])
                    outMoney += purchasePrice * i[4]
                    inMoney += i[5]
                    midstr = i[8] + "," + str(i[4]) + i[9] + "," + "共" + str(i[5]) + "元"
                    resultInfo.append(midstr)
            else:
                print("未查询到数据")
            resultString = "卖出了" + str(inMoney) + "元" + ";" + "成本" + str(outMoney) + "元" + ";" + "利润" + str(
                inMoney - outMoney) + "元"
            if nouns == "goods":
                print(resultInfo)
            if nouns == "money":
                print(resultString)
        if action == "ac_purchase" and nouns == "goods":
            result = queryPurchase.query_byDate(companyId, start, end)
            finalresult = []
            outMoneyarray = []
            outMoney = 0
            size = len(result)
            if size >= 1:
                for buy in result:
                    mid = "购入 " + buy[2] + " " + str(buy[5]) + "个" + "，单价" + str(buy[6]) + "元"
                    outMoney += float(buy[4]) * float(buy[5])
                    finalresult.append(mid)
            else:
                print("未查询到数据")
            outString = "进货支出" + str(outMoney) + "元"
            outMoneyarray.append(outString)
            print(finalresult)
        if action == "ac_query" and (nouns == "goods" or nouns == "store"):
            for i in range(0, len(final)):
                if final[i] == "库存":
                    a = i - 1
            print(final[a])
            if final[a] in goods or final[a] in ac_query:
                data = {"companyId": "5"}
                _resp = requests.post(url='http://127.0.0.1:5000/queryStoreGoods', json=data)
                resp_json = _resp.text
                print(resp_json)
            else:
                data = {"companyId": "5",
                        "name":final[a]}
                _resp = requests.post(url='http://127.0.0.1:5000/queryStoreGoods', json=data)
                resp_json = _resp.text
                print(resp_json)

        if action == "ac_out_money" and nouns == "money":
            result = queryPurchase.query_byDate(companyId, start, end)
            outMoneyarray = []
            outMoney = 0
            size = len(result)
            if size >= 1:
                for buy in result:
                    outMoney += float(buy[4]) * float(buy[5])
            else:
                print("未查询到数据")
            outString = "进货支出" + str(outMoney) + "元"
            outMoneyarray.append(outString)
            print(outMoneyarray)
