from app.utils.DBHelper import MyHelper


class UserDao:

    def queryAll(self):
        connection = MyHelper()
        return connection.executeQuery('select * from User')

    def add(self, account, password, companyid):
        connection = MyHelper()
        connection.executeUpdate('insert into User(account, \
        password, CompanyId, ID, phone, position) \
         values (%s,%s,%s)', [account, password, companyid])
