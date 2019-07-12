#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import uuid
import json
import jieba
import datetime
from flask import Blueprint, render_template, request
from app.dao.WareHouseDao import WareHouseDao
from app.dao.PurchaseDao import PurchaseDao
from app.utils.timeProcess import timeProcess
from app.dao.SellDao import SellDao
from app.dao.GoodsDao import GoodsDao

lanprocess = Blueprint("lanprocess", __name__)
#自然语言处理
@lanprocess.route("/languageProcess", methods=["GET", "POST"])
def languageProcess():
    _json = request.json
    companyId = _json.get('companyId')
    date = _json.get('date')
    language = _json.get('language')
    jieba.load_userdict("../app/utils/dict.txt")
    # 去除停用词
    stopwords = {}.fromkeys(['的', '包括', '等', '是', '多少'])
    time1 = ['今天', '这一天']
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
    # 对行为进行判断
    if action == 1:
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
        if nouns == 1:
            return resultInfo
        if nouns == 2:
            return resultString
    if action == 2 and nouns == 1:
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
            finalresult.append("未查询到数据")
        outString = "进货支出" + str(outMoney) + "元"
        outMoneyarray.append(outString)
        return finalresult
    if action == 3 and (nouns == 1 or nouns == 3):
        return ("仓库还剩的货")
    if action == 4 and nouns == 2:
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
        return outMoneyarray


