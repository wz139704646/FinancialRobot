from flask import Flask
from app.views.client import client
from app.views.wx import wx

# from app.views.smsVertify import sms

from app.views.web import web
from app.views.picUpload import up




def create_app():
    app = Flask(__name__)
    app.register_blueprint(wx)
    app.register_blueprint(client, url_prefix='/client')
    app.register_blueprint(web)
    app.register_blueprint(up, url_prefix='/pic')

    return app
