from redis import Redis

host = '47.100.244.29'
port = 3306
user = "root"
password = "Wdrs14569*"
charset = "utf8"

dbname = "financialrobot"

redis_port = 6379
redis_db = 0
redis_store = Redis(host=host, port=redis_port, db=redis_db, password='Wdrs14569*', decode_responses=True)
SECRET_KEY = 'WDRSZXNSHQBND11rZJYYnjhjKKXX'
JWT_HEADER_NAME = 'HTTP_TOKEN'
BIGCHAINDB_URL = 'http://47.100.244.29:9984/'
MONGO_URI = 'mongodb://47.100.244.29:27017/bigchain'
