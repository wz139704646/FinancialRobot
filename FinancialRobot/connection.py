import pymysql
def add():
    conn = pymysql.connect(
        host='42.159.81.168',
        port=3306,
        db="test",
        user="root",
        password="Wdrs145669***",
        charset="utf8"
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