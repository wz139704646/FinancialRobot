from app.utils.DBHelper import MyHelper


class CompanyDao:
    def queryAll(self):
        conn = MyHelper()
        return conn.executeQuery("select * from Company")

    def add(self, id, name, place):
        conn = MyHelper()
        conn.executeUpdate("insert into Company (id, name, place) VALUES (%s,%s,%s)", [id, name, place])



