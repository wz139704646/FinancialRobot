from flask import Flask, request
from app.views.client import client
from app.views.wx import wx

# from app.views.smsVertify import sms

from app.views.web import web
from app.views.picUpload import up
from app.views.languageProcess import lanprocess



def create_app():
    app = Flask(__name__)
    app.register_blueprint(wx)
    app.register_blueprint(client, url_prefix='/client')
    app.register_blueprint(web)
    app.register_blueprint(lanprocess)
    app.register_blueprint(up, url_prefix='/pic')

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
