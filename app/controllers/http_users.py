from app.model import catalogo
from flask import Blueprint, jsonify, request

from app.model import db
from app.controllers.http_security import current_user, roles_required
from app.view.serializers import user_json
from app.model.validation import password_value
from app.model.usuarios import create_user, delete_user, update_user

users_api = Blueprint("users_api", __name__)


@users_api.get("/users")
@roles_required("administrador", "bibliotecario")
def users():
    return jsonify({"items": [user_json(x) for x in catalogo.people()]})


@users_api.post("/users")
@roles_required("administrador")
def create_user_api():
    payload = request.get_json(silent=True) or {}
    try:
        user = create_user(payload["name"], payload["email"], payload["role"],
                           password_value(payload["password"]), payload.get("documento_identidad"))
    except (KeyError, ValueError) as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400
    return jsonify({"user": user_json(user)}), 201


@users_api.patch("/users/<int:user_id>")
@roles_required("administrador")
def edit_user(user_id: int):
    payload = request.get_json(silent=True) or {}
    try:
        user = update_user(
            user_id,
            payload.get("name"),
            payload.get("email"),
            payload.get("documento_identidad"),
        )
    except (ValueError) as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400
    return jsonify({"user": user_json(user)})


@users_api.delete("/users/<int:user_id>")
@roles_required("administrador")
def remove_user(user_id: int):
    if user_id == current_user().id:
        return jsonify(error="No puedes eliminar tu propia cuenta"), 400
    try:
        delete_user(user_id)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify({"message": "Usuario eliminado"})
