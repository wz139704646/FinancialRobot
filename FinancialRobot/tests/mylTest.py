import unittest
import base64
import binascii
from hashlib import sha1
from app.dao.CompanyDao import CompanyDao
from app.utils.DBHelper import MyHelper


class MylTest(unittest.TestCase):
    def test1(self):
        connect = MyHelper()
        result = connect.executeQuery("select * from student")
        print(result)

    def test2(self):
        com = CompanyDao()
        com.add('4', '诈骗公司', '北美')
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
