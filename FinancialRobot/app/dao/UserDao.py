from app.models.User import User
from app.utils.DBHelper import MyHelper
import json


class UserDao:
    @classmethod
    def to_dict(cls, data):
        result = []
        for row in data:
            res = {}
            res['account'] = row[0]
            res['password'] = row[1]
            res['companyId'] = row[2]
            res['ID'] = row[3]
            res['position'] = row[4]
            result.append(res)
        return result

    def query_all(self):
        connection = MyHelper()
        result = connection.executeQuery('select * from User')
        return result

    def add(self, account, password, companyid):
        connection = MyHelper()
        connection.executeUpdate('insert into User(account, \
        password, CompanyId, ID, phone, position) \
         values (%s,%s,%s)', [account, password, companyid])

    def query_by_account(self, account):
        helper = MyHelper()
        return helper.executeQuery("select * from User where account=%s", [account])

    def query_check_login(self, account, password):
        helper = MyHelper()
        return helper.executeQuery("select * from User where account=%s and password=%s ",
                                   [account, password])
