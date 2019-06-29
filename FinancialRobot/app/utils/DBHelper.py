import pymysql
from app import config


class MyHelper():

    def connection(self):
        try:
            self.conn = pymysql.connect(host=config.host,
                                        port=config.port,
                                        user=config.user,
                                        passwd=config.password,
                                        db=config.dbname,
                                        charset=config.charset)
        except Exception as e:
            print(e)
        self.cls = self.conn.cursor()
        print(self.conn)

    def free(self):
        self.cls.close()
        self.conn.close()

    def executeUpdate(self, sql, param=[]):
        try:
            self.connection()
            row = self.cls.execute(sql, param)
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            self.free()
        return row

    def executeQuery(self, sql, param=[]):
        try:
            self.connection()
            self.cls.execute(sql, param)
            result = self.cls.fetchall()
        except Exception as e:
            print(e)
        finally:
            self.free()
        return result
