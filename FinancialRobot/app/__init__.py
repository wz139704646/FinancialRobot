from flask import Flask, request
from flask_pymongo import PyMongo

from app.views.bigdb import big_db
from app.views.trans import trans
from app.views.wx import wx
from app.config import MONGO_URI
# from app.views.smsVertify import sms
from app.views.InOutMoney import inout_Money
from app.views.web import web
from app.views.picUpload import up
from app.utils.languageProcess import lanprocess


def create_app():
    app = Flask(__name__)

    app.register_blueprint(wx)
    app.register_blueprint(big_db)
    app.register_blueprint(trans, url_prefix='/trans')
    app.register_blueprint(web)
    app.register_blueprint(inout_Money)
    app.register_blueprint(lanprocess)
    app.register_blueprint(up, url_prefix='/pic')

    app.config["MONGO_URI"] = MONGO_URI
    # mongo = PyMongo(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
            headers = request.headers.get('Access-Control-Request-Headers')
            if headers:
                response.headers['Access-Control-Allow-Headers'] = headers
        return response

    return app
