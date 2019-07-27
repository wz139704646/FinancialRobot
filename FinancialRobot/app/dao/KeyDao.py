from app.utils.BigchainUtils import BigchainUtils
from app.utils.DBHelper import MyHelper
import json


class KeyDao:
    @classmethod
    def to_dict(cls, data):
        result = []
        for row in data:
            res = {'id': row[0], 'private_key': row[1], 'public_key': row[2]}
            result.append(res)
        return result

    def addKeys(self, _id):
        keys = BigchainUtils.gen_random_keypair()
        print(keys)
        connection = MyHelper()
        return connection.executeUpdate("insert into UserKeys (userId, privateKey, publicKey) VALUES (%s,%s,%s)",
                                        [_id, keys.private_key, keys.public_key])

    def queryKeys(self, _id):
        connection = MyHelper()
        return connection.executeQuery("select * from UserKeys where userId = %s", [_id])
