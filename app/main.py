from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from app.model import db # importar la base de datos desde modelo

import os
from datetime import timedelta
from secrets import token_hex


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///biblioteca.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", token_hex(32))
    WEB_ORIGIN = os.getenv("WEB_ORIGIN", "http://localhost:3000")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "0") == "1"
    APP_ENV = os.getenv("APP_ENV", "development")
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    MAX_CONTENT_LENGTH = 16384



#db = SQLAlchemy()


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    if app.config["APP_ENV"] == "production" and not os.getenv("SECRET_KEY"):
        raise ValueError("SECRET_KEY es obligatorio en producción")
    db.init_app(app)
    CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": app.config["WEB_ORIGIN"]}})

    from app.controllers.cli import register_cli
    from app.controllers.http import register_api
    register_cli(app)
    register_api(app)

    with app.app_context():
        from app.model import biblioteca,material, persona, prestamo  # noqa: F401
        db.create_all() #crea las tablas en la bd
    return app
