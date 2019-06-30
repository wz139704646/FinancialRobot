from flask import Blueprint, render_template

auth = Blueprint("auth", __name__)


@auth.route("/")
def hello():
    return render_template("index.html")
