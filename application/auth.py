from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    flash,
    make_response,
)
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
)
from .models import User
from . import db

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=username)
        response = make_response(redirect(url_for("main.dashboard")))
        set_access_cookies(response, access_token)
        flash("Logged in successfully!", "success")
        return response
    else:
        flash("Invalid credentials", "danger")
        return redirect(url_for("main.home"))


@auth.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        flash("Please provide both username and password", "warning")
        return redirect(url_for("main.home"))

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        flash("Username already exists", "danger")
        return redirect(url_for("main.home"))

    new_user = User(username=username)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    flash("Registration successful! You can now log in.", "success")
    return redirect(url_for("main.home"))


@auth.route("/logout", methods=["POST"])
def logout():
    response = make_response(redirect(url_for("main.home")))
    unset_jwt_cookies(response)
    flash("Logged out successfully!", "success")
    return response
