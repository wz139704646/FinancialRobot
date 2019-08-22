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
                with open(filename, encoding='UTF-8') as fr:
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

    # 执行事务，若其中一句出错，则整个事务撤销
    def executeUpdateTransaction(self, sqls=[], filename='', params=[]):
        try:
            self.connection()
            if len(sqls):
                try:
                    rows = 0
                    for i in range(0, len(sqls)):
                        rows += self.cls.execute(sqls[i], params[i])
                    self.conn.commit()
                    return rows
                except Exception as e1:
                    self.conn.rollback()
                    print("事务出错", e1)
            elif filename:
                with open(filename) as fr:
                    sql_file = fr.read()
                commands = sql_file.split(';')
                try:
                    rows = 0
                    for command in commands:
                        rows += self.cls.execute(command)
                    self.conn.commit()
                    return rows
                except Exception as e2:
                    self.conn.rollback()
                    print("事务出错", e2)
        except Exception as e3:
            print("其他错误", e3)
        finally:
            self.free()
