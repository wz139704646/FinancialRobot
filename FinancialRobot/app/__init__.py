from flask import Flask
from app.views.client import client
from app.views.auth import auth


def create_app():
    app = Flask(__name__)
    app.register_blueprint(auth)
    app.register_blueprint(client, url_prefix='/client')
    return app
