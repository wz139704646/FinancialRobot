# !/usr/bin/env python
# -*- coding:utf-8 -*-
#
# from app.utils.DBHelper import MyHelper
#
#
# class COHDao:
#     @classmethod
#     def to_dict(cls, data):
#         result = []
#         for row in data:
#             res = {}
#             res['id'] = row[0]
#             res['date'] = row[1]
#             res['variation'] = row[2]
#             res['changeDescription'] = row[3]
#             result.append(res)
#         return result
#
#     def queryNow(self):
#         conn = MyHelper()
#         return conn.executeQuery("select * from CashOnHand order by date desc ")
#
#     def queryAll(self):
#         conn = MyHelper()
#         return conn.executeQuery("select * from CashOnHand order by date")
#
#     def query_by_date(self, start, end):
#         connection = MyHelper()
#         return connection.executeQuery("select * from CashOnHand where date >= %s and date <%s order by date ",
#                                        [start, end])
#
#     def add(self, id, date, variation, changeDescription):
#         conn = MyHelper()
#         row = conn.executeUpdate(
#             "insert into CashOnHand (id, date,variation,changeDescription) VALUES (%s,%s,%s,%s)",
#             [id, date,  variation, changeDescription])
#         return row
from app.utils.bigchaindb_utils import *
from app.utils.mongodb_utils import *
import time
import datetime
import uuid


def str_to_unix(string):
    return int(time.mktime(datetime.datetime.strptime(string, '%Y-%m-%d %H:%M:%S').timetuple()))

def unix_to_date(unix):
    return datetime.datetime.fromtimestamp(unix)

class COHDao:

    def __init__(self):
        self.mongo = MongodbUtils()
        self.bigchain = BigchainUtils()

    @classmethod
    def to_dict(cls, data):
        result = []
        for i in data:
            i["data"]["date"] = unix_to_date(i["data"]["date"])
            result.append(i["data"])
        return result

    def queryNow(self):
        uuid_list = self.mongo.find_assets_uuid(keyword={"data.asset_type":"现金"})
        # return list(self.mongo.find_assets(keyword={"data.asset_type":"现金"},size=None).sort(
        result = []
        for i in uuid_list:
            asset = self.mongo.find_one_asset(asset_id=i["_id"])
            if asset:
                result.append(asset)
        return result


    def queryAll(self):
        return self.queryNow()

    def query_by_date(self, start, end):
        start_time = str_to_unix(start)
        end_time = str_to_unix(end)
        keyword = {
            "data.asset_type": "现金",
            "data.date": {
                "$gt": start_time,
                "$lt": end_time
            }
        }
        uuid_list = self.mongo.find_assets_uuid(keyword=keyword)
        result = []
        for i in uuid_list:
            asset = self.mongo.find_one_asset(asset_id=i)
            if asset:
                result.append(asset)
        return result

    def add(self, id, date, variation, changeDescription):
        bdb = BigchainUtils()
        company = BigchainUtils.get_keypair("company_id")
        asset_data = {
            "asset_type": "现金",
            "id": id,
            "uuid": id,
            "date": str_to_unix(date),
            "variation": str(variation),
            "changeDescription": changeDescription,
            "edition": time.time()
        }
        metadata = {
            "asset_type": "现金",
            "id": id,
            "edition": asset_data["edition"]
        }
        asset = bdb.create_asset(signer=company, asset=asset_data, metadata=metadata)
        if not asset:
            raise RuntimeError("bigchain insert error")
        return 1
