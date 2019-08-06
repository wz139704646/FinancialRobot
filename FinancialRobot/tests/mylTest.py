import time
import unittest
import base64
import binascii
import json
import jieba
from hashlib import sha1

from app.dao.CompanyDao import CompanyDao
from app.dao.GoodsDao import GoodsDao
from app.dao.UserDao import UserDao
from app.dao.WareHouseDao import WareHouseDao
from app.utils.MongoUtils import MongoUtils
from app.utils.BigchainUtils import BigchainUtils
from app.utils.DBHelper import MyHelper
from app.utils.json_util import *
import requests


class MylTest(unittest.TestCase):
    def test1(self):
        userdao = UserDao()
        result = userdao.query_all()
        j = json.dumps(return_success(""))
        print(j)

    def test2(self):
        com = CompanyDao()
        # com.add('4', '诈骗公司', '北美')
        print(com.queryAll())

    def test3(self):
        a = '123456'
        s = sha1()
        s.update(a.encode('utf-8'))
        c = s.digest()
        print(c)
        b = base64.b64encode(c)
        print(b)
        d = b.decode()
        print(d)
        e = base64.b64decode(b)
        f = binascii.hexlify(e)
        print(str(f, 'utf-8'))

    def test4(self):
        goods_dao = GoodsDao()
        add = goods_dao.add("手机", 20, "1", "电子", "kg")
        # res = goods_dao.query_all()
        # res = goods_dao.query_by_companyId('1', '苹', None)
        # j = json.dumps(return_success({'goodsList': GoodsDao.to_dict(res)}), cls=DecimalEncoder, ensure_ascii=False)
        print(add)

    def test5(self):
        print(json.dumps(return_unsuccess("失败")))

    def test6(self):
        text = "我来到清华大学"
        seg_list = jieba.cut(text, cut_all=True)
        print(u"[全模式]:", "/".join(seg_list))

    def test7(self):
        mongo = MongoUtils.get_mongo()
        trans = mongo.db.transactions.find({"operation": "TRANSFER"})
        print(list(trans))

    def test8(self):
        goods = GoodsDao()
        res = goods.query_by_warehouse("5", None)
        print(json.dumps(GoodsDao.to_ware_dict(res), cls=DecimalEncoder, ensure_ascii=False))

    def test9(self):
        url = 'http://127.0.0.1:5000/decodeToken'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzAxODExODAsImlhdCI6MTU2NDk5NzE4MCwiZGF0YSI6eyJhY2NvdW50IjoiMTU3NzEwMDA1ODciLCJsb2dpbl90aW1lIjoxNTY0OTk3MTgwfX0.4tLyLrPOFK32uByDRaSLE4VmUv_9h6LTI1sVLnu81zc'
        }
        payload = {
            'token': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzAxODExODAsImlhdCI6MTU2NDk5NzE4MCwiZGF0YSI6eyJhY2NvdW50IjoiMTU3NzEwMDA1ODciLCJsb2dpbl90aW1lIjoxNTY0OTk3MTgwfX0.4tLyLrPOFK32uByDRaSLE4VmUv_9h6LTI1sVLnu81zc'
        }
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        print(r.text)

    def test10(self):
        res = UserDao().add_permission_by_role('15771000587', 'admin')
        print(res)

    def test11(self):
        res = UserDao().del_permission_by_features('15771000587', ['Common'])
        print(res)
