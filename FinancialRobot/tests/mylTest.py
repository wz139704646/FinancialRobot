
import unittest
import base64
import binascii
import jieba
from hashlib import sha1
from app.config import redis_store
from app.dao.BankStatementDao import BankStatementDao
from app.dao.CompanyDao import CompanyDao
from app.dao.GoodsDao import GoodsDao
from app.dao.UserDao import UserDao
from app.utils.json_util import *
import requests


class MylTest(unittest.TestCase):
    def test1(self):
        userdao = UserDao()
        result = userdao.query_all()
        print(result)
        j = json.dumps(return_success(UserDao.to_dict(result)))
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
        pass
        # mongo = MongoUtils.get_mongo()
        # trans = mongo.db.transactions.find({"operation": "TRANSFER"})
        # print(list(trans))

    def test8(self):
        goods = GoodsDao()
        res = goods.query_by_warehouse("5", None)
        print(json.dumps(GoodsDao.to_ware_dict(res), cls=DecimalEncoder, ensure_ascii=False))

    def test9(self):
        url = 'http://127.0.0.1:5000/login'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzA1NDA0MjYsImlhdCI6MTU2NTM1NjQyNiwiZGF0YSI6eyJhY2NvdW50IjoiMTczNzE0NDkwMjUiLCJsb2dpbl90aW1lIjoxNTY1MzU2NDI2fX0.AyaskCtQXXmbj4TPkrn4KORESEKf532FSgEnsWU11Zs'
        }

        r = requests.get(url, headers=headers)
        print(r.text)

    def test10(self):
        res = UserDao().query_all()
        for r in res:
            print(r[0])
            res = UserDao().add_permission_by_role(r[0], 'admin')
        print(res)

    def test10_1(self):
        res = UserDao().add_permission_by_role('13474709706', 'admin')
        print(res)

    def test11(self):
        res = UserDao().del_permission_by_features('15771000587', ['Common', 'Data Analysis'])

        print(res)

    def test12(self):
        store = base64.b64decode(
            "MCwwLDAsNywwLDAsMCwwLDAsMCwwLDQsMCwwLDAsMCwwLDAsMC…wLDgsMCwwLDAsOSwwLDAsMCw0LDAsMCwwLDEsMCwwLDAsMA==")
        print(store)
        store_in = binascii.hexlify(store)
        print(store_in)
        strpass = str(store_in, 'utf-8')
        print(strpass)

    def test13(self):
        redis_store.delete('access_token')
        print(redis_store.get('access_token'))

    def test14(self):
        res = GoodsDao().query_by_warehouse("5", None, None, None)
        print(res)

    def test15(self):
        res = GoodsDao().query_store_by_goods_id('5', '81e40a91-6554-3605-824b-d944634c1d71')
        print(res)

    def test16(self):
        res = BankStatementDao().queryAll()
        print(res)

    def test17(self):
        res = BankStatementDao().queryByName('珞珈山人民银行')
        print(res)

    def test18(self):
        res = BankStatementDao().querySumAmount()
        print(res)

    def test19(self):
        res = BankStatementDao().update("9f4bd060-85fa-3f47-b1f6-6d9e1ed1ffc9")
        print(res)

    def test20(self):
        res = datetime.datetime.now()
        print(str(res))
