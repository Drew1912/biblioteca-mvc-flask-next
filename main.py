from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from app.settings import Config


db = SQLAlchemy()


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    db.init_app(app)
    CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": app.config["WEB_ORIGIN"]}})

    from app.controllers.cli import register_cli
    from app.api import register_api
    register_cli(app)
    register_api(app)

    with app.app_context():
        from app.model import material, persona, prestamo  # noqa: F401
    return app


app = create_app()
