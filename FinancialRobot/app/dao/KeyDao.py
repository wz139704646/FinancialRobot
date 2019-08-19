from app.utils.BigchainUtils import BigchainUtils
from app.utils.DBHelper import MyHelper
import json


class KeyDao:
    @classmethod
    def to_dict(cls, data):
        result = []
        for row in data:
            res = {'account': row[0], 'private_key': row[1], 'public_key': row[2], 'userId': row[3]}
            result.append(res)
        return result

    def addKeys(self, account, userId=None):
        keys = BigchainUtils.gen_random_keypair()
        print(keys)
        connection = MyHelper()
        return connection.executeUpdate("insert into UserKeys (account, privateKey, publicKey,userId)"
                                        " VALUES (%s,%s,%s,%s)",
                                        [account, keys.private_key, keys.public_key, userId])

    def queryKeys(self, _id):
        connection = MyHelper()
        return connection.executeQuery("select * from UserKeys where account = %s", [_id])

    def query_private_key(self, _id):
        connection = MyHelper()
        return connection.executeQuery("select privateKey from UserKeys where account = %s", [_id])

    def query_public_key(self, _id):
        connection = MyHelper()
        return connection.executeQuery("select * from UserKeys where account = %s", [_id])
