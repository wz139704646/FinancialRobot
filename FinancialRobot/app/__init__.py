from flask import Flask, request
from app.views.bigdb import big_db
from app.views.trans import trans
from app.views.wx import wx
from app.config import MONGO_URI
from app.views.InOutMoney import inout_Money
from app.views.picUpload import up
from app.views.goods import goods
from app.views.customer import customer
from app.views.supplier import supplier
from app.views.company import company
from app.views.warehouse import warehouse
from app.views.sell import sell
from app.views.purchase import purchase
from app.utils.languageProcess import lanprocess
from app.utils.auth import *


def create_app():
    app = Flask(__name__)

    app.register_blueprint(wx)
    app.register_blueprint(goods)
    app.register_blueprint(warehouse)
    app.register_blueprint(sell)
    app.register_blueprint(purchase)
    app.register_blueprint(big_db)
    app.register_blueprint(trans, url_prefix='/trans')
    app.register_blueprint(supplier)
    app.register_blueprint(company)
    app.register_blueprint(customer)
    app.register_blueprint(inout_Money)
    app.register_blueprint(lanprocess)
    app.register_blueprint(up, url_prefix='/pic')

    app.config["MONGO_URI"] = MONGO_URI

    # mongo = PyMongo(app)

    @app.before_request
    # @check_token
    def res():
        print(request.path)

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
