#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, request
from app.dao.COHDao import COHDao
from app.dao.BankStatementDao import BankStatementDao
from app.dao.DailyfundDao import DailyfundDao
from app.utils.json_util import *
import uuid
import datetime
import time
import json

inout_Money = Blueprint("inout_Money", __name__)


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


# 查询所有现金流动记录
@inout_Money.route("/queryAllCashRecord", methods=["GET"])
def queryAllCashRecord():
    query = COHDao()
    result = query.queryAll()
    size = len(result)
    if size == 0:
        return json.dumps(return_unsuccess('Error: No data'))
    else:
        return json.dumps(return_success(COHDao.to_dict(result)), ensure_ascii=False, cls=DecimalEncoder)


# 录入银行存/取款记录
@inout_Money.route("/addBankRecord", methods=["GET", "POST"])
def addBankRecord():
    query = BankStatementDao()
    _json = request.json
    voucher = _json.get('voucher')
    bankName = _json.get('bankName')
    companyName = _json.get('companyName')
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


def InsertDailyfund(date, changeDescription, amount):
    query = DailyfundDao()
    d = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    date_zero = d.replace(year=d.year, month=d.month, day=d.day, hour=0, minute=0, second=0)
    date_tomorrow = d.replace(year=d.year, month=d.month, day=d.day + 1, hour=0, minute=0, second=0)
    date_yesterday = d.replace(year=d.year, month=d.month, day=d.day - 1, hour=0, minute=0, second=0)
    result = query.query_by_date(date_zero)
    if len(result) == 0:
        yester_result = query.query_by_date(date_yesterday)
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
