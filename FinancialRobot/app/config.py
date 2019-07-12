from redis import Redis

host = '42.159.81.168'
port = 3306
user = "root"
password = "Wdrs145669***"
charset = "utf8"
dbname="FinancialRobot"
redis_port = 6379
redis_db = 0
redis_store = Redis(host=host, port=redis_port, db=redis_db, password='Wdrs14569***', decode_responses=True)
SECRET_KEY = 'WDRSZXNSHQBND11rZJYYnjhjKKXX'
JWT_HEADER_NAME = 'HTTP_TOKEN'
