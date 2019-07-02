from app.utils.DBHelper import MyHelper

class CompanyDao:
    @classmethod
    def to_dict(cls, data):
        result = []
        for row in data:
            res = {}
            res['id'] = row[0]
            res['name'] = row[1]
            res['place'] = row[2]
            result.append(res)
        return result
    def queryAll(self):
        conn = MyHelper()
        return conn.executeQuery("select * from Company")

    def query_cname_cplace(self):
        conn = MyHelper()
        return conn.executeQuery("select name,place from Company")

    def add(self, id, name, place):
        conn = MyHelper()
        conn.executeUpdate("insert into Company (id, name, place) VALUES (%s,%s,%s)", [id, name, place])



