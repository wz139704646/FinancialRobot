#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import unittest
import requests
import uuid
import json
import jieba
from flask import Blueprint, render_template, request
from app.dao.WareHouseDao import WareHouseDao
from app.utils.DBHelper import MyHelper
from app.dao.CompanyDao import CompanyDao
from app.dao.CustomerDao import CustomerDao
from app.dao.SupplierDao import SupplierDao
from app.dao.GoodsDao import GoodsDao
from app.dao.UserDao import UserDao
from app.utils.res_json import *

lanprocess = Blueprint("lanprocess", __name__)

#自然语言处理
@lanprocess.route("/languageProcess", methods=["GET", "POST"])
def languageProcess():
    jieba.load_userdict("../app/utils/dict.txt")
    times=['今天','这一天','昨天','上一天','这周','上一周','上周','这个月','上个月']
    action=['赚','挣','卖','收入','盈利','进账']
    nouns=['钱','东西','商品','货']
    text1 = "上一周赚了多少钱"
    text2 = "今天卖了多少东西"
    text3 = "看一下库存"
    seg_list1 = jieba.cut(text1, cut_all=False)
    seg_list2 = jieba.cut(text2, cut_all=False)
    seg_list3 = jieba.cut(text3, cut_all=False)
    print(u"[精确模式]", "/".join(seg_list1))
    print(u"[精确模式]", "/".join(seg_list2))
    print(u"[精确模式]", "/".join(seg_list3))
