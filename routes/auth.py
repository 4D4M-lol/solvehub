from flask import Blueprint, render_template, request, redirect, url_for, session
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

from models.user import User

auth = Blueprint("auth", __name__)

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    username = request.form["username"]
    password = request.form["password"]

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return "Username already exists."

    password_hash = generate_password_hash(password)

    user = User(
        username=username,
        password_hash=password_hash
    )

    db.session.add(user)
    db.session.commit()

    return redirect(url_for("auth.login"))

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        session["user_id"] = user.id
        session["username"] = user.username

        return redirect(url_for("main.home"))

    return "Invalid username or password."

@auth.route("/logout")
def logout():
    session.clear()

    return redirect(url_for("main.home"))