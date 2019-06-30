import unittest

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
