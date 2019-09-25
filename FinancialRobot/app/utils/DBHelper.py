import pymysql
import threading
from app import config
from DBUtils.PooledDB import PooledDB

class MyHelper(object):
    # _instance_lock = threading.Lock()
    __pool = None

    def __init__(self):
        self.pool = PooledDB(
            # 使用链接数据库的模块import pymysql
            creator=pymysql,
            # 连接池允许的最大连接数，0和None表示不限制连接数
            maxconnections=6,
            # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            mincached=2,
            # 链接池中最多闲置的链接，0和None不限制
            maxcached=5,
            # 链接池中最多共享的链接数量，0和None表示全部共享。
            # 因为pymysql和MySQLdb等模块的 threadsafety都为1，
            # 所有值无论设置为多少，maxcached永远为0，所以永远是所有链接都共享。
            maxshared=3,
            # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            blocking=True,
            # 一个链接最多被重复使用的次数，None表示无限制
            maxusage=None,
            # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            setsession=[],
            # ping MySQL服务端，检查是否服务可用。
            #  如：0 = None = never, 1 = default = whenever it is requested,
            # 2 = when a cursor is created, 4 = when a query is executed, 7 = always
            ping=0,

            # 数据库信息
            host=config.host,
            port=config.port,
            user=config.user,
            password=config.password,
            database=config.dbname,
            charset=config.charset
        )

    # x线程安全的单例模式
    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(MyHelper, "_instance"):
    #         with MyHelper._instance_lock:
    #             if not hasattr(MyHelper, "_instance"):
    #                 MyHelper._instance = object.__new__(cls)
    #     return MyHelper._instance

    def connection(self):
        try:
            self.conn = self.pool.connection()
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
