import unittest
import base64
import binascii
import json
from hashlib import sha1

from app.dao.CompanyDao import CompanyDao
from app.dao.GoodsDao import GoodsDao
from app.dao.UserDao import UserDao
from app.utils.DBHelper import MyHelper
from app.utils.decimal_encoder import DecimalEncoder
from app.utils.res_json import *


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
        # goods_dao.add("苹果", 20, "2", "食品", "kg")
        # res = goods_dao.query_all()
        res = goods_dao.query_by_companyId('1', '苹', None)
        j = json.dumps(return_success({'goodsList': GoodsDao.to_dict(res)}), cls=DecimalEncoder, ensure_ascii=False)
        print(j)
        b = json.loads(j)
        print(b)

    def test5(self):
        print(json.dumps(return_unsuccess("失败")))

    def test6(self):
        con=MyHelper()
