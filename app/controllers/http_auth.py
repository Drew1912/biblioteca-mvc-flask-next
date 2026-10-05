from flask import Blueprint, jsonify, request, session
from app.controllers.http_guards import csrf_token
from app.controllers.http_security import current_user
from app.view.serializers import user_json
from app.model.usuarios import authenticate

auth_api = Blueprint("auth_api", __name__)


@auth_api.post("/login")
def login():
    payload = request.get_json(silent=True) or {}
    user = authenticate(str(payload.get("email", "")), str(payload.get("password", "")))
    if user is None:
        return jsonify({"error": "Credenciales inválidas"}), 401
    session.clear()
    session["user_id"] = user.id
    session.permanent = True
    return jsonify({"user": user_json(user), "csrfToken": csrf_token()})


@auth_api.post("/logout")
def logout():
    session.clear()
    return jsonify({"message": "Sesión cerrada"})


@auth_api.get("/me")
def me():
    user = current_user()
    if user is None:
        return jsonify({"user": None, "csrfToken": csrf_token()}), 200
    return jsonify({"user": user_json(user), "csrfToken": csrf_token()})
