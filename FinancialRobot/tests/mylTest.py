import unittest
import base64
from app.dao.CompanyDao import CompanyDao
from app.utils.DBHelper import MyHelper


class MylTest(unittest.TestCase):
    def test1(self):
        connect = MyHelper()
        result = connect.executeQuery("select * from Warehouse")
        print(result)

    def test2(self):
        com = CompanyDao()
        #com.add('4', '诈骗公司', '北美')
        print(com.queryAll())

    def test3(self):
        a = 'sadfsd98'
        b = base64.b64encode(a.encode('utf-8'))
        print(str(b, 'utf-8'))
        b = base64.b64decode(b)
        print(str(b, 'utf-8'))