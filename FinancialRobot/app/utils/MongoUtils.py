from flask_pymongo import PyMongo

from manage import app


class MongoUtils:
    @staticmethod
    def get_mongo():
        return PyMongo(app)
