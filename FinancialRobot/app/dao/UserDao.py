from app.models.User import User
from app.utils.DBHelper import MyHelper
import json


class UserDao:
    @classmethod
    def to_dict(cls, data):
        result = []
        for row in data:
            res = {'account': row[0], 'password': row[1], 'companyId': row[2], 'ID': row[3], 'position': row[4],
                   'openid': row[5]}
            result.append(res)
        return result

    def query_all(self):
        connection = MyHelper()
        result = connection.executeQuery('select * from User')
        return result

    def query_permission(self, account):
        connection = MyHelper()
        return connection.executeQuery("select feature from Permission where account = %s", [account])

    def add(self, account, password, companyid):
        connection = MyHelper()
        row = connection.executeUpdate('insert into User(account, \
        password, CompanyId) \
         values (%s,%s,%s)', [account, password, companyid])
        return row

    def query_by_account(self, account):
        helper = MyHelper()
        return helper.executeQuery("select * from User where account=%s", [account])

    def query_check_login(self, account, password):
        helper = MyHelper()
        return helper.executeQuery("select * from User where account=%s and password=%s ",
                                   [account, password])

    def query_by_openid_account(self, account, openid):
        _param = []
        _sql = "select * from User where 1=1"
        if account:
            _sql += " and account = %s"
            _param.append(account)
        if openid:
            _sql += " and openid = %s"
            _param.append(openid)
        helper = MyHelper()
        return helper.executeQuery(_sql, _param)

    def bind_wx(self, account, openid):
        helper = MyHelper()
        return helper.executeUpdate("update User set openid = %s where account = %s",
                                    [openid, account])
