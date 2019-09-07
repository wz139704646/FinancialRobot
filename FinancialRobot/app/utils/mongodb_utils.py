import pymongo
from app.config import MONGO_URI

class MongodbUtils():


    def __init__(self):
        self.myclient = pymongo.MongoClient(MONGO_URI)
        self.db = self.myclient.bigchain

    def find_assets_uuid(self,keyword):
        return list(self.db.assets.aggregate([{"$match":keyword},{"$group":{"_id":"$data.uuid"}}]))

    def find_assets(self,keyword=None,page=0,size=10):
        # return self.db.assets.find(keyword)[page*size:page*size+size]
        if page is not None and size is not None:
            return self.db.assets.find(keyword).limit(size).skip(page*size)
        else:
            return self.db.assets.find(keyword)

    def find_one_asset(self, asset_id):
        return self.db.assets.find({"data.uuid":asset_id}).sort("data.edition",-1)[0]

    def count_assets(self,keyword=None):
        return self.db.assets.find(keyword).count()

    def find_one_metadata(self,id):
        return self.db.metadata.find_one({"id":id})

    def find_transactions(self,asset_id, operation=None):
        keyword = {"asset.id":asset_id}
        if operation:
            keyword["operation"] = operation
        return self.db.transactions.find(keyword).sort("inputs.date",-1)

    def find_latest_transaction(self,asset_id, operation=None):
        keyword = {"asset.id": asset_id}
        if operation:
            keyword["operation"] = operation
        # return self.db.transactions.aggregate({"$group": {"_id": "max", "max_value": {"$max": "$inputs.date"}}})
        # return self.db.transactions.find(keyword).sort("inputs.date",-1)