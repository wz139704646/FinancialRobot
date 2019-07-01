from flask import Flask
from app.views.client import client
from app.views.wx import wx
from app.views.web import web


def create_app():
    app = Flask(__name__)
    app.register_blueprint(wx, url_prefix='/wx')
    app.register_blueprint(client, url_prefix='/client')
    app.register_blueprint(web, url_prefix='/web')
    return app

