import pymysql
import threading
from app import config


class MyHelper(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    # x线程安全的单例模式
    def __new__(cls, *args, **kwargs):
        if not hasattr(MyHelper, "_instance"):
            with MyHelper._instance_lock:
                if not hasattr(MyHelper, "_instance"):
                    MyHelper._instance = object.__new__(cls)
        return MyHelper._instance

    def connection(self):
        try:
            self.conn = pymysql.connect(host=config.host,
                                        port=config.port,
                                        user=config.user,
                                        passwd=config.password,
                                        db=config.dbname,
                                        charset=config.charset)
            self.cls = self.conn.cursor()
        except Exception as e:
            print(e)

    def free(self):
        try:
            self.cls.close()
        except Exception as e:
            print(e)
        try:
            self.conn.close()
        except Exception as e:
            print(e)

    def executeUpdate(self, sql, param=[]):
        try:
            self.connection()
            row = self.cls.execute(sql, param)
            self.conn.commit()
            return row
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            self.free()

    def executeQuery(self, sql, param=[]):
        try:
            self.connection()
            self.cls.execute(sql, param)
            result = self.cls.fetchall()
            return result
        except Exception as e:
            print(e)
        finally:
            self.free()

    def executeCreate(self, sql='', filename='', param=[]):
        try:
            self.connection()
            if sql:
                self.cls.execute(sql, param)
            elif filename:
                with open(filename) as fr:
                    sql_file = fr.read()
                commands = sql_file.split(';')
                for command in commands:
                    try:
                        self.cls.execute(command)
                    except Exception as e1:
                        print(e1)
        except Exception as e2:
            print(e2)
        finally:
            self.free()
