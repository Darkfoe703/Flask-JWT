from flask import Flask, redirect, url_for, flash
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Set JWT cookies
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_SECURE"] = False  # True on production over HTTPS
    app.config["JWT_COOKIE_HTTPONLY"] = True
    app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
    app.config["JWT_REFRESH_COOKIE_PATH"] = "/"
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # True on production

    # Init SQLAlchemy
    db.init_app(app)

    # Init JWT
    jwt = JWTManager(app)

    # blueprints
    from .auth import auth
    from .routes import main

    app.register_blueprint(auth)
    app.register_blueprint(main)

    # Error handler: invalid or missing JWT
    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        flash("You need to log in to access this page.")
        return redirect(url_for("main.home"))

    # Error handler: expired token
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        flash("Your session has expired. Please log in again.")
        return redirect(url_for("main.home"))

    with app.app_context():
        db.create_all()  # Create DB tables

    return app
