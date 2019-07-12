from flask import Blueprint, render_template

trans = Blueprint("trans", __name__)


@trans.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")
