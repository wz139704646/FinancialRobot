#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from flask import Blueprint, request
from app.dao.COHDao import COHDao
from app.dao.CompanyDao import CompanyDao
from app.dao.BankStatementDao import BankStatementDao
from app.dao.DailyfundDao import DailyfundDao
from app.utils.json_util import *
from app.utils.timeProcess import timeProcess
import uuid
import datetime
import time
import json

inout_Money = Blueprint("inout_Money", __name__)


# 查询现金记录
def queryCash(start, end):
    query = COHDao()
    result = query.query_by_date(start, end)
    return result


# 查询银行记录
def queryBank(start, end):
    query = BankStatementDao()
    result = query.query_by_date(start, end)
    return result


# 查询日报表
def queryDaily(start, end):
    query = DailyfundDao()
    result = query.query_by_SD(start, end)
    return result


def InsertDailyfund(date, changeDescription, amount):
    query = DailyfundDao()
    d = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    date_zero = d.replace(year=d.year, month=d.month, day=d.day, hour=0, minute=0, second=0)
    result = query.query_by_date(date_zero)
    if len(result) == 0:
        yester_result = query.queryAll()
        if len(yester_result) == 0:
            yesterMoney = 0
            row = query.add(yesterMoney, changeDescription, amount, amount, date_zero)
            return row
        else:
            yesterMoney = yester_result[0][2]
            row = query.add(yesterMoney, changeDescription, amount, amount, date_zero)
            return row
    else:
        originExplain = result[0][1]
        originMoney = result[0][2]
        originChange = result[0][3]
        nowExplain = originExplain + changeDescription
        nowMoney = originMoney + amount
        nowChange = originChange + amount
        row = query.InsertToday(nowExplain, nowMoney, nowChange, date_zero)
        return row


# 录入现金流通记录
@inout_Money.route("/addCashRecord", methods=["GET", "POST"])
def addCashRecord():
    query = COHDao()
    _json = request.json
    date = _json.get('date')
    variation = float(_json.get('variation'))
    changeDescription = _json.get('changeDescription')
    id = str(uuid.uuid3(uuid.NAMESPACE_OID, str(date)))
    nowResult = query.queryNow()
    length = len(nowResult)
    if length >= 1:
        originValue = nowResult[0][2]
    else:
        originValue = 0
    balance = variation + originValue
    row = query.add(id, date, balance, originValue, variation, changeDescription)
    insertDailyRow = InsertDailyfund(date, changeDescription, variation)
    if row == 1:
        if insertDailyRow == 1:
            return json.dumps(return_success('Add succeed！'))
        else:
            return json.dumps(return_unsuccess('Error: Daily fund add failed,cash add succeed'))
    else:
        return json.dumps(return_unsuccess('Error: Add failed'))


# 录入银行存/取款记录
@inout_Money.route("/addBankRecord", methods=["GET", "POST"])
def addBankRecord():
    query = BankStatementDao()
    queryName = CompanyDao()
    _json = request.json
    voucher = _json.get('voucher')
    bankName = _json.get('bankName')
    companyId = _json.get('companyId')
    comResult = queryName.queryNameById(companyId)
    if len(comResult) == 1:
        companyName = comResult[0][0]
        clearForm = _json.get('clearForm')
        amount = float(_json.get('amount'))
        date = _json.get('date')
        status = "未核对"
        bankResult = query.queryByName(bankName)
        if len(bankResult) == 0:
            balance = amount
        else:
            balance = bankResult[0][7] + amount
        sumResult = query.queryNow()
        if len(sumResult) == 0:
            sumBalance = balance
        else:
            sumBalance = sumResult[0][8] + amount
        print(voucher, bankName, companyName, clearForm, amount, date, status, balance, sumBalance)
        row = query.add(voucher, bankName, companyName, clearForm, amount, date, status, balance, sumBalance)
        changeDescription = "在 " + bankName + clearForm + str(abs(amount)) + "元  "
        insertDailyRow = InsertDailyfund(date, changeDescription, amount)
        if row == 1:
            if insertDailyRow == 1:
                return json.dumps(return_success('Add succeed！'))
            else:
                return json.dumps(return_unsuccess('Error: Daily fund add failed,bank add succeed'))
        else:
            return json.dumps(return_unsuccess('Error: Add failed'))
    else:
        return json.dumps(return_unsuccess('Error: CompanyId error!'))


# 查询所有现金记录
@inout_Money.route("/queryAllCashRecord", methods=["GET", "POST"])
def queryAllCashRecord():
    query = COHDao()
    result = query.queryAll()
    if len(result) >= 1:
        return json.dumps(return_success(COHDao.to_dict(result)), ensure_ascii=False, cls=DecimalEncoder)
    else:
        return json.dumps(return_success('Sorry,no data'))


# 根据日期查询现金记录
@inout_Money.route("/queryCashRecordByDate", methods=["GET", "POST"])
def queryCashRecordByDate():
    _json = request.json
    start = _json.get('start')
    end = _json.get('end')
    result = queryCash(start, end)
    if len(result) >= 1:
        return json.dumps(return_success(COHDao.to_dict(result)), ensure_ascii=False, cls=DecimalEncoder)
    else:
        return json.dumps(return_success('Sorry,no data'))


# 根据选项查询现金记录
@inout_Money.route("/queryCashRecordByOption", methods=["GET", "POST"])
def queryCashRecordByOption():
    _json = request.json
    date = _json.get('date')
    option = int(_json.get('option'))
    d = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    if option == 1 or option == 2 or option == 3:
        if option == 1:
            start = d.replace(year=d.year, month=d.month, day=d.day, hour=0, minute=0, second=0)
            end = d.replace(year=d.year, month=d.month, day=d.day + 1, hour=0, minute=0, second=0)
        if option == 2:
            monday = timeProcess.get_current_week(d)
            start = monday.replace(year=monday.year, month=monday.month, day=monday.day, hour=0, minute=0, second=0)
            delta = datetime.timedelta(days=7)
            end = start + delta
        if option == 3:
            start = d.replace(year=d.year, month=d.month, day=1, hour=0, minute=0, second=0)
            end = d.replace(year=d.year, month=d.month + 1, day=1, hour=0, minute=0, second=0)
        result = queryCash(start, end)
        print(start, end)
        if len(result) >= 1:
            return json.dumps(return_success(COHDao.to_dict(result)), ensure_ascii=False, cls=DecimalEncoder)
        else:
            return json.dumps(return_success('Sorry,no data'))
    else:
        return json.dumps(return_unsuccess('Error!'))


# 查询所有银行记录
@inout_Money.route("/queryAllBankRecord", methods=["GET", "POST"])
def queryAllBankRecord():
    query = BankStatementDao()
    result = query.queryAll()
    if len(result) >= 1:
        return json.dumps(return_success(BankStatementDao.to_dict(result)), ensure_ascii=False, cls=DecimalEncoder)
    else:
        return json.dumps(return_success('Sorry,no data'))


# 根据日期查询银行记录
@inout_Money.route("/queryBankRecordByDate", methods=["GET", "POST"])
def queryBankRecordByDate():
    _json = request.json
    start = _json.get('start')
    end = _json.get('end')
    result = queryBank(start, end)
    if len(result) >= 1:
        return json.dumps(return_success(BankStatementDao.to_dict(result)), ensure_ascii=False, cls=DecimalEncoder)
    else:
        return json.dumps(return_success('Sorry,no data'))


# 根据选项查询银行记录
@inout_Money.route("/queryBankRecordByOption", methods=["GET", "POST"])
def queryBankRecordByOption():
    _json = request.json
    date = _json.get('date')
    option = int(_json.get('option'))
    d = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    if option == 1 or option == 2 or option == 3:
        if option == 1:
            start = d.replace(year=d.year, month=d.month, day=d.day, hour=0, minute=0, second=0)
            end = d.replace(year=d.year, month=d.month, day=d.day + 1, hour=0, minute=0, second=0)
        if option == 2:
            monday = timeProcess.get_current_week(d)
            start = monday.replace(year=monday.year, month=monday.month, day=monday.day, hour=0, minute=0, second=0)
            delta = datetime.timedelta(days=7)
            end = start + delta
        if option == 3:
            start = d.replace(year=d.year, month=d.month, day=1, hour=0, minute=0, second=0)
            end = d.replace(year=d.year, month=d.month + 1, day=1, hour=0, minute=0, second=0)
        result = queryBank(start, end)
        print(start, end)
        if len(result) >= 1:
            return json.dumps(return_success(BankStatementDao.to_dict(result)), ensure_ascii=False, cls=DecimalEncoder)
        else:
            return json.dumps(return_success('Sorry,no data'))
    else:
        return json.dumps(return_unsuccess('Error!'))


# 查询日报表所有记录
@inout_Money.route("/queryAllDailyfund", methods=["GET", "POST"])
def queryAllDailyfund():
    query = DailyfundDao()
    result = query.queryAllDaily()
    if len(result) >= 1:
        return json.dumps(return_success(DailyfundDao.to_dict(result)), ensure_ascii=False, cls=DecimalEncoder)
    else:
        return json.dumps(return_success('Sorry,no data'))


# 根据日期查询日报表
@inout_Money.route("/queryDailyByDate", methods=["GET", "POST"])
def queryDailyByDate():
    _json = request.json
    start = _json.get('start')
    end = _json.get('end')
    result = queryDaily(start, end)
    if len(result) >= 1:
        return json.dumps(return_success(DailyfundDao.to_dict(result)), ensure_ascii=False, cls=DecimalEncoder)
    else:
        return json.dumps(return_success('Sorry,no data'))


# 根据选项查询日报表
@inout_Money.route("/queryDailyByOption", methods=["GET", "POST"])
def queryDailyByOption():
    _json = request.json
    date = _json.get('date')
    option = _json.get('option')
    d = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    if option == 1 or option == 2 or option == 3:
        if option == 1:
            start = d.replace(year=d.year, month=d.month, day=d.day, hour=0, minute=0, second=0)
            end = d.replace(year=d.year, month=d.month, day=d.day + 1, hour=0, minute=0, second=0)
        if option == 2:
            monday = timeProcess.get_current_week(d)
            start = monday.replace(year=monday.year, month=monday.month, day=monday.day, hour=0, minute=0, second=0)
            delta = datetime.timedelta(days=7)
            end = start + delta
        if option == 3:
            start = d.replace(year=d.year, month=d.month, day=1, hour=0, minute=0, second=0)
            end = d.replace(year=d.year, month=d.month + 1, day=1, hour=0, minute=0, second=0)
        result = queryDaily(start, end)
        print(start, end)
        if len(result) >= 1:
            return json.dumps(return_success(DailyfundDao.to_dict(result)), ensure_ascii=False, cls=DecimalEncoder)
        else:
            return json.dumps(return_success('Sorry,no data'))
    else:
        return json.dumps(return_unsuccess('Error!'))


# 审核银行记录
@inout_Money.route("/checkBankStatus", methods=["GET", "POST"])
def checkBankStatus():
    query=BankStatementDao()
    _json = request.json
    voucher = _json.get('voucher')
    row=query.update(voucher)
    if row== 1:
        return json.dumps(return_success("修改成功"))
    else:
        return json.dumps(return_success('修改失败'))
