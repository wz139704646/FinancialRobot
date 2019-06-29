import pymysql
from app import config
def add():
    conn = pymysql.connect(
        host=config.host,
        port=config.port,
        user=config.user,
        password=config.password,
        charset=config.charset,
        db="test",
    )
    print(conn)
    # 游标
    cls=conn.cursor()
    # row = cls.execute("insert into orders value (1,2,null,null)")


    cls.execute("select * from student")
    c = cls.fetchall()
    print(c)

    cls.close()
    conn.close()
add()