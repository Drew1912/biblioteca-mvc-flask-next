from secrets import compare_digest, token_urlsafe
from flask import jsonify, request, session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.model.transaction import rollback_session


def csrf_token():
    if "csrf" not in session:
        session["csrf"] = token_urlsafe(32)
    return session["csrf"]


def register_guards(app):
    @app.before_request
    def protect_write():
        if not request.path.startswith("/api/") or request.method in {"GET", "HEAD", "OPTIONS"}:
            return None
        origin = request.headers.get("Origin")
        if origin != app.config["WEB_ORIGIN"]:
            return jsonify(error="Origen no permitido"), 403
        if not session.get("csrf") or not compare_digest(
            request.headers.get("X-CSRF-Token", ""), session["csrf"]
        ):
            return jsonify(error="Sesión de formulario inválida. Actualiza la página."), 403
        if request.is_json and request.content_length and not isinstance(request.get_json(silent=True), dict):
            return jsonify(error="Se esperaba un objeto JSON"), 400

    @app.after_request
    def security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        if request.path.startswith("/api/"):
            response.headers["Cache-Control"] = "no-store"
        return response

    @app.errorhandler(ValueError)
    @app.errorhandler(TypeError)
    @app.errorhandler(KeyError)
    def invalid_data(error):
        rollback_session()
        return jsonify(error="Datos inválidos"), 400

    @app.errorhandler(IntegrityError)
    def conflict(error):
        rollback_session()
        return jsonify(error="Registro duplicado o con historial asociado"), 409

    @app.errorhandler(SQLAlchemyError)
    def persistence_error(error):
        rollback_session()
        app.logger.exception("Error de persistencia")
        return jsonify(error="No se pudo guardar la operación"), 503
