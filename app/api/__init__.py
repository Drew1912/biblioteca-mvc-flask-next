from flask import Flask

from app.api.auth import auth_api
from app.api.resources import resources_api


def register_api(app: Flask) -> None:
    app.register_blueprint(auth_api, url_prefix="/api/v1/auth")
    app.register_blueprint(resources_api, url_prefix="/api/v1")
