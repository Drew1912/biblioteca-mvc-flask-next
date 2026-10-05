from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.controllers.http_auth import auth_api
from app.controllers.http_materials import materials_api
from app.controllers.http_users import users_api
from app.controllers.http_loans import loans_api
from app.controllers.http_reports import reports_api
from app.controllers.http_guards import register_guards


def register_api(app: Flask) -> None:
    limiter = Limiter(get_remote_address, app=app, storage_uri=app.config.get("RATELIMIT_STORAGE_URI", "memory://"))
    register_guards(app)
    app.register_blueprint(auth_api, url_prefix="/api/v1/auth")
    app.view_functions["auth_api.login"] = limiter.limit("10 per minute")(app.view_functions["auth_api.login"])
    for blueprint in (materials_api, users_api, loans_api, reports_api):
        app.register_blueprint(blueprint, url_prefix="/api/v1")

    @app.get("/api/v1/health")
    def health():
        return {"status": "ok"}
