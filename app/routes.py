from flask import Blueprint, render_template, redirect,url_for, flash
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import jwt_required, get_jwt_identity


main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("home.html")


@main.route("/dashboard")
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()
    return render_template("dashboard.html", username=current_user)
