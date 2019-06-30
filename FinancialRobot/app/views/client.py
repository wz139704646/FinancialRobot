from flask import Blueprint, render_template

client = Blueprint("client", __name__)


@client.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")
