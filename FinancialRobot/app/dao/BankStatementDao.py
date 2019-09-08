#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# from app.utils.DBHelper import MyHelper
#
#
# class BankStatementDao:
#     @classmethod
#     def to_dict(cls, data):
#         result = []
#         for row in data:
#             res = {}
#             res['voucher'] = row[0]
#             res['bankName'] = row[1]
#             res['companyName'] = row[2]
#             res['clearForm'] = row[3]
#             res['amount'] = row[4]
#             res['date'] = row[5]
#             res['status'] = row[6]
#             res['balance'] = row[7]
#             result.append(res)
#         return result
#
#     def queryByName(self, bankName):
#         conn = MyHelper()
#         return conn.executeQuery("select * from BankStatement where bankName = %s order by date desc ", [bankName])
#
#     def queryNow(self):
#         conn = MyHelper()
#         return conn.executeQuery("select * from BankStatement order by date desc ")
#
#     def queryAll(self):
#         conn = MyHelper()
#         return conn.executeQuery("select * from BankStatement order by date")
#
#     def querySumAmount(self):
#         conn = MyHelper()
#         return conn.executeQuery("select SUM(amount) from BankStatement")
#
#     def query_by_date(self, start, end):
#         connection = MyHelper()
#         return connection.executeQuery("select * from BankStatement where date >= %s and date <%s order by date ",
#                                        [start, end])
#
#     def add(self, voucher, bankName, companyName, clearForm, amount, date, status, balance):
#         conn = MyHelper()
#         row = conn.executeUpdate(
#             "insert into BankStatement (voucher, bankName, companyName,clearForm,amount,date,status,balance) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
#             [voucher, bankName, companyName, clearForm, amount, date, status, balance])
#         return row
#
#     def update(self, voucher):
#         conn = MyHelper()
#         row = conn.executeUpdate("Update BankStatement Set status ='已核对' Where voucher =%s", [voucher])

from app.utils.bigchaindb_utils import *
from app.utils.mongodb_utils import *
import time
import datetime


def str_to_unix(string):
    return int(time.mktime(datetime.datetime.strptime(string, '%Y-%m-%d %H:%M:%S').timetuple()))


def unix_to_date(unix):
    return datetime.datetime.fromtimestamp(unix)


class BankStatementDao:
    def __init__(self):
        self.mongo = MongodbUtils()
        self.bigchain = BigchainUtils()

    @classmethod
    def to_dict(cls, data):
        result = []
        for row in data:
            row["data"]["date"] = unix_to_date(row["data"]["date"])
            row['data']['amount'] = float(row['data']['amount'])
            row['data']['balance'] = float(row['data']['balance'])
            result.append(row["data"])
        return result

    def queryByName(self, bankName):
        keyword = {
            "data.asset_type": "BankStatement",
            "data.bankName": bankName
        }
        uuid_list = self.mongo.find_assets_uuid(keyword=keyword)
        result = []
        for i in uuid_list:
            asset = self.mongo.find_one_asset(asset_id=i["_id"])
            if asset:
                result.append(asset)
        return result

    def queryNow(self):
        uuid_list = self.mongo.find_assets_uuid(keyword={"data.asset_type": "BankStatement"})
        result = []
        for i in uuid_list:
            asset = self.mongo.find_one_asset(asset_id=i["_id"])
            if asset:
                # meta = self.mongo.db.metadata.find_one({'metadata.voucher': i["_id"]})
                # asset['data']['status'] = meta['metadata']['status']
                # asset['data']['edition'] = meta['metadata']['edition']
                result.append(asset)
        return result

    def queryAll(self):
        return self.queryNow()

    def querySumAmount(self):
        uuid_list = self.mongo.find_assets_uuid(keyword={"data.asset_type": "BankStatement"})
        sum_amount = 0
        for i in uuid_list:
            asset = self.mongo.find_one_asset(asset_id=i["_id"])
            if asset:
                sum_amount = sum_amount + float(asset['data']['amount'])
        return sum_amount

    def query_by_date(self, start, end):
        start_time = str_to_unix(start)
        end_time = str_to_unix(end)
        keyword = {
            "data.asset_type": "BankStatement",
            "data.date": {
                "$gt": start_time,
                "$lt": end_time
            }
        }
        uuid_list = self.mongo.find_assets_uuid(keyword=keyword)
        result = []
        for i in uuid_list:
            asset = self.mongo.find_one_asset(asset_id=i["_id"])
            if asset:
                result.append(asset)
        return result

    def add(self, voucher, bankName, companyName, clearForm, amount, date, status, balance):
        bdb = BigchainUtils()
        company = BigchainUtils.get_keypair("company_id")
        asset_data = {
            "asset_type": "BankStatement",
            "uuid": voucher,
            "voucher": voucher,
            "bankName": bankName,
            "companyName": companyName,
            "clearForm": clearForm,
            "amount": str(amount),
            "date": str_to_unix(date),
            "status": status,
            "balance": str(balance),
            "edition": time.time()
        }
        metadata = {
            "asset_type": "BankStatement",
            "voucher": voucher,
            "status": asset_data["status"],
            "edition": asset_data["edition"]
        }
        asset = bdb.create_asset(signer=company, asset=asset_data, metadata=metadata)
        if not asset:
            raise RuntimeError("bigchain insert error")
        return 1

    def update(self, voucher):
        # self.mongo.db.metadata.update({'metadata.voucher': voucher},
        #                               {"$set": {"metadata.status": "已审核", "edition": time.time()}})
        asset = self.mongo.find_one_asset(asset_id=voucher)['data']
        print(asset)
        self.add(asset['voucher'], asset['bankName'], asset['companyName'], asset['clearForm'], asset['amount'],
                 str(unix_to_date(asset['date'])), '已审核', asset['balance'])
        return 1
