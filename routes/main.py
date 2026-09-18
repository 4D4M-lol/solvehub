from flask import Blueprint, render_template, redirect, url_for, session
from extensions import db

from models.user import User

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("home.html")

@main.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = db.session.get(User, session["user_id"])

    return render_template("profile.html", user=user)