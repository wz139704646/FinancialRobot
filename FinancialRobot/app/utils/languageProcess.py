#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import uuid
import json
import jieba
import os
import datetime
from app.utils.json_util import *
from flask import Blueprint, render_template, request
from app.dao.WareHouseDao import WareHouseDao
from app.dao.PurchaseDao import PurchaseDao
from app.utils.timeProcess import timeProcess
from app.dao.SellDao import SellDao
from app.dao.GoodsDao import GoodsDao

lanprocess = Blueprint("lanprocess", __name__)


# 自然语言处理
@lanprocess.route("/languageProcess", methods=["GET", "POST"])
def languageProcess():
    _json = request.json
    print(_json)
    companyId = _json.get('companyId')
    date = _json.get('time')
    language = _json.get('language')
    # language="今天花了多少钱"
    UPLOAD_FOLDER = '../utils/dict.txt'
    basedir = os.path.abspath(os.path.dirname(__file__))
    file_dir = os.path.join(basedir, UPLOAD_FOLDER)

    jieba.load_userdict(file_dir)
    # 去除停用词
    stopwords = {}.fromkeys(['的', '包括', '等', '是', '多少'])
    today = ['今天', '这一天']
    yesterday = ['昨天', '上一天']
    thisWeek = ['这周', '这一周']
    lastWeek = ['上周', '上一周']
    thisMonth = ['这个月']

    acInmoney = ['赚', '挣', '卖', '收入', '盈利', '进账']
    acPurchase = ['进', '买']
    acQuery = ['查', '看', '查看']
    acOutmoney = ['花', '消费', '支出']

    goods = ['东西', '商品', '货']
    money = ['钱']
    store = ['库存']
    # 精确模式
    segs = jieba.cut(language, cut_all=False)
    final = []
    for seg in segs:
        if seg not in stopwords:
            final.append(seg)
    print(final)
    time = 1
    for item in final:
        if time == 1:
            if item in yesterday:
                time = 2
            if item in thisWeek:
                time = 3
            if item in lastWeek:
                time = 4
            if item in thisMonth:
                time = 5
        if item in acInmoney:
            action = 1
        if item in acPurchase:
            action = 2
        if item in acQuery:
            action = 3
        if item in acOutmoney:
            action = 4
        if item in goods:
            nouns = 1
        if item in money:
            nouns = 2
        if item in store:
            nouns = 3

    querySell = SellDao()
    queryPurchase = PurchaseDao()
    inputTime = datetime.datetime.strptime(date, '%Y-%m-%d')

    # 对时间进行判断
    if time == 1:
        delta = datetime.timedelta(days=1)
        n_days = inputTime + delta
        end = n_days.strftime('%Y-%m-%d %H:%M:%S')
        start = inputTime
    if time == 2:
        delta = datetime.timedelta(days=1)
        n_days = inputTime - delta
        start = n_days.strftime('%Y-%m-%d %H:%M:%S')
        end = inputTime
    if time == 3:
        start = timeProcess.get_current_week(inputTime)
        delta = datetime.timedelta(days=7)
        end = start + delta
    if time == 4:
        end = timeProcess.get_current_week(inputTime)
        delta = datetime.timedelta(days=7)
        start = end - delta
    if time == 5:
        start = datetime.date(inputTime.year, inputTime.month - 1, 1)
        end = datetime.date(inputTime.year, inputTime.month, 1) - datetime.timedelta(1)
    print(start)
    print(end)
    print(action)
    print(nouns)
    # 对行为进行判断
    if action == 1:
        resultInfo = []
        resultArray = []
        resultString = ""
        inMoney = 0
        outMoney = 0
        result = querySell.query_byDate(companyId, start, end)
        print(result)
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
        if nouns == 1:
            return json.dumps(return_success(resultInfo), ensure_ascii=False)
            # return resultInfo

        if nouns == 2:
            resultArray.append(resultString)
            return json.dumps(return_success(resultArray), ensure_ascii=False)

    if action == 2 and nouns == 1:
        result = queryPurchase.query_byDate(companyId, start, end)
        finalresult = []
        outMoneyarray = []
        outMoney = 0
        size = len(result)
        print(result)
        if size >= 1:
            for buy in result:
                mid = "购入 " + buy[2] + " " + str(buy[5]) + "个" + "，单价" + str(buy[6]) + "元"
                aa = float(buy[5]) * float(buy[6])
                print(aa)
                outMoney += aa
                finalresult.append(mid)
        else:
            finalresult.append("未查询到数据")
        outString = "进货支出" + str(outMoney) + "元"
        outMoneyarray.append(outString)
        return json.dumps(return_success(finalresult), ensure_ascii=False)

    if action == 3 and (nouns == 1 or nouns == 3):
        return ("仓库还剩的货")
    if action == 4 and nouns == 2:
        result = queryPurchase.query_byDate(companyId, start, end)
        outMoneyarray = []
        outMoney = 0
        print(result)
        size = len(result)
        if size >= 1:
            for buy in result:
                aa = float(buy[5]) * float(buy[6])
                print(aa)
                outMoney += aa

        else:
            print("未查询到数据")
        outString = "进货支出" + str(outMoney) + "元"
        outMoneyarray.append(outString)
        return json.dumps(return_success(outMoneyarray), ensure_ascii=False)
