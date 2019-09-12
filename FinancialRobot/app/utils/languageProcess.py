#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import uuid
import json
import jieba
import time
import os
import requests
import datetime
from app.utils.json_util import *
from flask import Blueprint, render_template, request
from app.dao.WareHouseDao import WareHouseDao
from app.dao.SupplierDao import SupplierDao
from app.dao.SellDao import SellDao
from app.dao.GoodsDao import GoodsDao
from app.dao.PurchaseDao import PurchaseDao
from app.utils.timeProcess import timeProcess
from app.utils.mongodb_utils import MongodbUtils
from app.utils.auth import Auth

lanprocess = Blueprint("lanprocess", __name__)
UPLOAD_FOLDER = '../utils/dict.txt'
basedir = os.path.abspath(os.path.dirname(__file__))
file_dir = os.path.join(basedir, UPLOAD_FOLDER)
jieba.load_userdict(file_dir)

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
LOCATE = 'http://47.100.244.29:5000'

mongo = MongodbUtils()


def computeLanguage(items, time):
    for item in items:
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
    return time,action,nouns


# 对时间进行判断
def judgeTime(time,d):
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
        newDay = d.replace(year=d.year, month=d.month, day=d.day, hour=0, minute=0, second=0)
        end = timeProcess.get_current_week(newDay)
        delta = datetime.timedelta(days=7)
        start = end - delta
    if time == "this_month":
        start = d.replace(year=d.year, month=d.month, day=1, hour=0, minute=0, second=0)
        end = d.replace(year=d.year, month=d.month + 1, day=1, hour=0, minute=0, second=0)
    return start,end


# 获取一定时间内的销售数据
def getSellData(SellResult,time,start,end):
    finalResult=[]
    if SellResult['success'] == True:
        sellResult = SellResult['result']
        print(sellResult)
        groups = []
        group = {}
        goodsType = []
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
        if time == 'this_month':
            finalResult.append(GetPictureSellData(start, end))
        GetPicSellPriceResult=GetPicSellPrice(goodsType, sellResult)
        finalResult.append(GetPicSellPriceResult[0])
        sellInfo = {'type': 'collapse-group',
                    'summary': '该段时间共卖出'+str(GetPicSellPriceResult[1])+'种商品，共计'+str(GetPicSellPriceResult[2])+'元',
                    'groups': groups}
        finalResult.append(sellInfo)
        return json.dumps(return_success(finalResult))
    else:
        return json.dumps(return_unsuccess(SellResult['errMsg']))


# 获取一定时间内的进货数据
def getPurchaseData(Purchase,time,start,end):
    finalResult=[]
    if Purchase['success'] == True:
        purchaseResult = Purchase['result']
        print(purchaseResult)
        groups = []
        goodsType = []
        group = {}
        activeNames = []
        items = []
        for sellRecord in purchaseResult:
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
        # 调用获取图片信息的函数
        GetPicPurchasePriceResult=GetPicPurchasePrice(goodsType, purchaseResult)
        finalResult.append(GetPicPurchasePriceResult[0])
        if time=='this_month':
            finalResult.append(GetPicturePurchaseData(start,end))
        groups.append(group)
        sellInfo = {'type': 'collapse-group',
                    'summary': '该段时间共进了'+str(GetPicPurchasePriceResult[1])+'种货物，共计'+str(GetPicPurchasePriceResult[2])+'元',
                    'groups': groups}
        finalResult.append(sellInfo)
        return json.dumps(return_success(finalResult))
    else:
        return json.dumps(return_unsuccess(Purchase['errMsg']))


# 获取商品库存信息
def getGoodsStore(final, headers):
    queryWare = WareHouseDao()
    Cusresult = queryWare.query_byCompanyId('5')
    print(Cusresult)
    if len(final) == 3:
        global goods
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
                goodsStore = requests.post(url=LOCATE + '/queryStoreGoods', data=data_json,
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
            return json.dumps(return_success(storeInfo))
        else:
            data = {'companyId': '5',
                    'name': final[1]}
            data_json = json.dumps(data, cls=DecimalEncoder)
            goodsStore = requests.post(url=LOCATE + '/queryStoreGoods', data=data_json,
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
                return json.dumps(return_success(storeInfo))
            else:
                return json.dumps(return_unsuccess(Goodsstore['errMsg']))
    else:
        data = {'companyId': '5',
                'name': final[2]}
        data_json = json.dumps(data, cls=DecimalEncoder)
        goodsStore = requests.post(url=LOCATE + '/queryStoreGoods', data=data_json, headers=headers)
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
            return json.dumps(return_success(storeInfo))
        else:
            return json.dumps(return_unsuccess(Goodsstore['errMsg']))


# 查询商品价格（进价、售价）
def getGoodsPrice(nouns, inRecords, outRecords):
    finalResult=[]
    judge = 0
    allgroups = []
    Picturedata = []
    averageInmoney = 0
    NewInmoney = 0
    averageOutmoney = 0
    NewOutmoney = 0
    if nouns == "price":
        judge = 1
    if inRecords['success'] == True and outRecords['success'] == True:
        if nouns == "inPrice" or judge == 1:
            if inRecords['success'] == True:
                inRecord = inRecords['result']
                # 画图数据
                datas1 ={}
                datas1['type']='line'
                ah={}
                # 表格数据
                groups = []
                group = {}
                items = []
                count = 0
                sumPrice = 0
                newPrice = 0
                for inGoods in inRecord:
                    # data 画图数据
                    ah[inGoods['date']] = inGoods['purchasePrice']
                    # item 表格数据
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
                group['title'] = '商品的进价情况'
                group['items'] = items
                allgroups.append(group)
                datas1['diagram']=ah
                Picturedata.append(datas1)
                groups.append(group)
                averageInmoney = round(sumPrice / count, 2)
                Price = {'type': 'list-group',
                         'summary': '商品最新进价为' + str(newPrice) + "元，平均进价为" + str(round(sumPrice / count, 2)) + "元",
                         'groups': groups}
                finalResult.append(datas1)
        if nouns == "outPrice" or judge == 1:
            if outRecords['success'] == True:
                inRecord = outRecords['result']
                datas2 = {}
                datas2['type'] = 'line'
                print(inRecord)
                groups = []
                group = {}
                items = []
                count = 0
                sumPrice = 0
                newPrice = 0
                ah={}
                for inGoods in inRecord:
                    ah[inGoods['date']] = inGoods['purchasePrice']
                    item = {}
                    item['title'] = inGoods['goodsName']
                    item['value'] = str(round(inGoods['sumprice'] / inGoods['number'], 2)) + "元"
                    sumPrice = sumPrice + inGoods['sumprice'] / inGoods['number']
                    NewOutmoney = newPrice = inGoods['sumprice'] / inGoods['number']
                    count = count + 1
                    item['label'] = '客户：' + inGoods['customerName']
                    item['tag'] = inGoods['date']
                    items.append(item)
                group['title'] = '商品的售价情况'
                group['items'] = items
                groups.append(group)
                allgroups.append(group)
                averageOutmoney = round(sumPrice / count, 2)
                Price = {'type': 'list-group',
                         'summary': '商品最新售价为' + str(newPrice) + "元，平均售价为" + str(round(sumPrice / count, 2)) + "元",
                         'groups': groups}
                datas2['diagram'] = ah
                finalResult.append(datas2)
        if nouns == "price":
            Price = {'type': 'list-group',
                     'summary': '商品最新售价为' + str(NewOutmoney) + "元，平均售价为" + str(
                         averageOutmoney) + "元 " + ' 商品最新进价为' + str(NewInmoney) + "元，平均进价为" + str(
                         averageInmoney) + "元",
                     'groups': allgroups}
        finalResult.append(Price)
        return json.dumps(return_success(finalResult))
    else:
        return json.dumps(return_unsuccess(inRecords['errMsg'] + outRecords['errMsg']))


# 获取一段时间内的资金收入/支出
def getInOutMoney(CashResult, BankResult, action):
    inBank = outBank = 0
    inCash = outCash = 0
    if CashResult['success'] == True and BankResult['success'] == True:
        if CashResult['success'] == True:
            cashResult = CashResult['result']
            for sinCash in cashResult:
                if sinCash['variation'] > 0:
                    inCash = inCash + sinCash['variation']
                else:
                    outCash = outCash + sinCash['variation']
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
            return json.dumps(return_success(inMoney))
        if action == "ac_out_money":
            outBank = abs(outBank)
            outCash = abs(outCash)
            summary = '现金支出' + str(outCash) + '元，银行存款、转账等支出' + str(outBank) + '元，共计' + str(outCash + outCash) + '元'
            outMoney = {'type': 'text',
                        'summary': summary}
            return json.dumps(return_success(outMoney))
    else:
        return json.dumps(return_unsuccess(CashResult['errMsg'] + BankResult['errMsg']))


# 获取客户信息
def getCustomerInfo(CustomerDaoResult, name):
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
        return json.dumps(return_success(supplierInfo))
    else:
        return json.dumps(return_unsuccess(CustomerDaoResult['errMsg']))


# 获取供应商信息
def getSupplierInfo(SupplierResult, name):
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
        return json.dumps(return_success(supplierInfo))
    else:
        return json.dumps(return_unsuccess(SupplierResult['errMsg']))


def record_api(data, user):
    mongo.myclient.record.apirecord.insert({
        "data": data,
        "record_time": datetime.datetime.now(),
        "user": user
    })


def GetPicturePurchaseData(start, end):
    queryForPic = PurchaseDao()
    PicResult = queryForPic.query_ForPic(start, end)
    datas = {}
    datas['type'] = 'line'
    ah={}
    for picData in PicResult:
        ah[picData[1]] = picData[0]
    datas['diagram']=ah
    return datas


def GetPictureSellData(start, end):
    queryForPic = SellDao()
    PicResult = queryForPic.query_ForPic(start, end)
    datas = {}
    ah={}
    datas['type'] = 'line'
    for picData in PicResult:
        ah[picData[1]] = picData[0]
    datas['diagram'] = ah
    return datas


def GetPicSellPrice(goodsType, sellResult):
    sumPriceByType = []
    sumNumByType = []
    for gType in goodsType:
        sumOneType = 0
        sumOneNum = 0
        sumPrice=0
        for sellRecord in sellResult:
            goodsList = sellRecord['goodsList']
            for goods in goodsList:
                goodsId = goods['goodsId']
                queryGoodsType = GoodsDao()
                sumPrice=sumPrice+goods['sumprice']
                goodType = queryGoodsType.queryType_byId(goodsId)
                if goodType[0][0] == gType:
                    sumOneType = sumOneType + goods['sumprice']
                    sumOneNum = sumOneNum + goods['number']
        sumPriceByType.append(sumOneType)
        sumNumByType.append(sumOneNum)
    datas = {}
    ah={}
    datas['type'] = 'pie'
    for i in range(0, len(sumPriceByType)):
        ah[goodsType[i]] = sumPriceByType[i]
    datas['diagram'] = ah
    return datas,len(goodsType),sumPrice


def GetPicPurchasePrice(goodsType, purchaseResult):
    sumPriceByType = []
    sumNumByType = []
    for gType in goodsType:
        sumOneType = 0
        sumOneNum = 0
        sumPrice=0
        for sellRecord in purchaseResult:
            goodsList = sellRecord['goodsList']
            for goods in goodsList:
                goodsId = goods['goodsId']
                queryGoodsType = GoodsDao()
                sumPrice=sumPrice+goods['number'] * goods['price']
                goodType = queryGoodsType.queryType_byId(goodsId)
                if goodType[0][0] == gType:
                    sumOneType = sumOneType + goods['number'] * goods['price']
                    sumOneNum = sumOneNum + goods['number']
        sumPriceByType.append(sumOneType)
        sumNumByType.append(sumOneNum)
    datas = {}
    ah={}
    datas['type'] = 'pie'
    for i in range(0, len(sumPriceByType)):
        ah[goodsType[i]] = sumPriceByType[i]
    datas['diagram']=ah
    return datas,len(goodsType),sumPrice


def getGoodsPricePic():
    print('caonima')


# 自然语言处理
@lanprocess.route("/languageProcess", methods=["GET", "POST"])
def languageProcess():
    _json = request.json
    date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    companyId = _json.get('companyId')
    language = _json.get('language')
    token = request.headers.get('Authorization')
    d = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    jieba.load_userdict("../app/utils/dict.txt")
    # 去除停用词
    stopwords = {}.fromkeys(['的', '包括', '等', '是', '多少', "所有", "一下"])
    # 精确模式
    segs = jieba.cut(language, cut_all=False)
    final = []
    for seg in segs:
        if seg not in stopwords:
            final.append(seg)
    print(final)
    Time = "today"
    computeResult=computeLanguage(final, Time)
    Time=computeResult[0]
    action=computeResult[1]
    nouns=computeResult[2]
    try:
        user_info = Auth.decode_jwt(token)
    except:
        return json.dumps({'auth': False, 'errMsg': 'token解码失败'})
    data = {
        "company_id": companyId,
        "time": Time,
        "action": action,
        "nouns": nouns
    }
    record_api(data, user_info)

    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    timeResult=judgeTime(Time,  d)
    start=timeResult[0]
    end=timeResult[1]
    # 对行为进行判断
    ##### 一段时期内的销售情况 #####
    if action == "ac_in_money" and nouns == "goods":
        data = {"start": start,
                "end": end,
                'companyId': '5',
                'date': "hh"}
        data_json = json.dumps(data, cls=DecimalEncoder)
        sellRecords = requests.post(url=LOCATE + '/querySell', data=data_json, headers=headers)
        if sellRecords.status_code == 200:
            SellResult = json.loads(sellRecords.content)
            return getSellData(SellResult,Time,start,end)
        else:
            return '不好意思，没有查到相关数据哦', sellRecords.status_code
    ##### 某段时间内进的货物 #####
    elif action == "ac_purchase" and nouns == "goods":
        data = {'companyId': '5',
                'date': "hh",
                'start': start,
                'end': end}
        data_json = json.dumps(data, cls=DecimalEncoder)
        purchaseRecords = requests.post(url=LOCATE + '/queryPurchase', data=data_json, headers=headers)
        if purchaseRecords.status_code == 200:
            SellResult = json.loads(purchaseRecords.content)
            return getPurchaseData(SellResult,Time,start,end)
        else:
            return '不好意思，没有查到相关数据哦', purchaseRecords.status_code
    ###### 查商品库存#####
    elif action == "ac_query" and (nouns == "goods" or nouns == "store"):
        return getGoodsStore(final, headers)
    # 查询商品的价格
    elif action == "ac_query" and (nouns == "price" or nouns == "inPrice" or nouns == "outPrice"):
        if len(final) == 3:
            data = {'name': final[1]}
        else:
            data = {'name': final[2]}
        data_json = json.dumps(data, cls=DecimalEncoder)
        _respOut = requests.post(url=LOCATE + '/SellPriceByName', data=data_json, headers=headers)
        outRecords = json.loads(_respOut.content)
        _respIn = requests.post(url=LOCATE + '/purchasePriceByName', data=data_json,
                                headers=headers)
        inRecords = json.loads(_respIn.content)

        if _respOut.status_code == 200 and _respIn.status_code == 200:
            return getGoodsPrice(nouns, inRecords, outRecords)
        else:
            return '不好意思，没有查到相关数据哦', _respOut.status_code, _respIn.status_code

    #### 一段时间的收入或支出####
    elif nouns == "money":
        data = {'start': start,
                'end': end}
        data_json = json.dumps(data, cls=DecimalEncoder)
        _respCash = requests.post(url=LOCATE + '/queryCashRecordByDate', data=data_json,
                                  headers=headers)
        CashResult = json.loads(_respCash.content)
        _respBank = requests.post(url=LOCATE + '/queryBankRecordByDate', data=data_json,
                                  headers=headers)
        BankResult = json.loads(_respBank.content)
        if _respCash.status_code == 200 and _respBank.status_code == 200:
            return getInOutMoney(CashResult, BankResult, action)
        else:
            return '不好意思，没有查到相关数据哦', _respCash.status_code, _respBank.status_code
    #####查询顾客信息#####
    elif action == "ac_query" and nouns == "customer":
        name = ''
        print(final[3])
        for i in range(2, len(final) - 1):
            if final[i] != '信息':
                name = name + final[i]
        print(name)
        data = {'companyId': '5',
                'name': name}
        data_json = json.dumps(data, cls=DecimalEncoder)
        _respCustomer = requests.post(url=LOCATE + '/queryCustomer', data=data_json, headers=headers)
        CustomerDaoResult = json.loads(_respCustomer.content)
        if _respCustomer.status_code == 200:
            return getCustomerInfo(CustomerDaoResult, name)
        else:
            return '不好意思，没有查到相关数据哦', _respCustomer.status_code
    #####查询供应商信息#####
    elif action == "ac_query" and nouns == "supplier":
        name = ''
        for i in range(2, len(final) - 1):
            if final[i] != '信息':
                name = name + final[i]
        print(name)
        data = {'companyId': '5',
                'name': name}
        data_json = json.dumps(data, cls=DecimalEncoder)
        _respSupplier = requests.post(url=LOCATE + '/querySupplierByName', data=data_json,
                                      headers=headers)
        SupplierResult = json.loads(_respSupplier.content)
        if _respSupplier.status_code == 200:
            return getSupplierInfo(SupplierResult, name)
        else:
            return '不好意思，没有查到相关数据哦', _respSupplier.status_code
    #####查询表格信息#####
    elif action == "ac_query" and nouns == "tables":
        return json.dumps(return_unsuccess('Sorry,no data'))
    else:
        return json.dumps(return_unsuccess('不好意思，我听不懂你在说什么'))
