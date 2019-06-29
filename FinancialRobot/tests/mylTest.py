import unittest
from app.utils.DBHelper import MyHelper


class MylTest(unittest.TestCase):
    def test1(self):
        connect = MyHelper()
        result = connect.executeQuery("select * from student")
        print(result)
