from app.utils.DBHelper import MyHelper


class UserDao:

    def queryAll(self):
        connection = MyHelper()
        return connection.executeQuery('select * from User')

    def add(self, account, password, companyid, id, phone, position):
        connection = MyHelper()
        connection.executeUpdate('insert into User(account, \
        password, CompanyId, ID, phone, position) \
         values (%s,%s,%s,%s,%s,%s)',[account, password, companyid, id, phone, position])

u=UserDao()
u.add('123','1','1','123','13asdf','asdf')
