import pymysql
from sshtunnel import SSHTunnelForwarder

with SSHTunnelForwarder(
        ('42.159.81.168',22),  # B机器的配置
        ssh_password='Wdrs14569***',
        ssh_username='jxHuang',
        remote_bind_address=('127.0.0.1', 3306)) as server:  # A机器的配置
    server.start()
    print(server.local_bind_port)
    db_connect = pymysql.connect(host='127.0.0.1',  # 此处必须是是127.0.0.1
                                 port=3306,
                                 db="test",
                                 user="root",
                                 password="Wdrs145669***",
                                 charset="utf8"
                                 )
    print(db_connect)
    cur = db_connect.cursor()
    cur.execute('select * from student')
    c=cur.fetchall()
    print(c)
