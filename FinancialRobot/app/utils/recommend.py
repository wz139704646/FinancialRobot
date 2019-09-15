from app.utils.mongodb_utils import *
import datetime
from datetime import timedelta
mongo = MongodbUtils()


def recommend(uid):
    record_aggregate_list = list(mongo.myclient.record.apirecord.aggregate([
        {
            "$match":{
                "user.data.account": uid,
                "data.time":{"$ne":""},
                "data.action":{"$ne":""},
                "data.nouns":{"$ne":""},
                "record_time":{"$gte":datetime.datetime.now() - timedelta(days=10)}
            }
        },
        {
            "$group":{
                "_id": {
                    "time":"$data.time",
                    "action":"$data.action",
                    "nouns":"$data.nouns"
                },
                "count":{"$sum":1}
            }
        },
        {
            "$sort":{
                "count":-1
            }
        }

    ]))

    result = []
    if len(record_aggregate_list) > 0:
        for i in record_aggregate_list[:3]:
             record_list = list(mongo.myclient.record.apirecord.find({
                "data.time":i["_id"]["time"],
                "data.action":i["_id"]["action"],
                "data.nouns":i["_id"]["time"],
                "data.language":{"$exists":True}
             }))
             if len(record_list) > 0:
                 result.append(record_list[-1]["data"]["language"])

    return result

