from flask import Blueprint, jsonify, request

from app.controllers.http_security import roles_required
from app.model.catalogo import people
from app.controllers.personas import create_member, delete_member, update_member
from app.model.validation import password_value
from app.view.serializers import user_json

readers_api = Blueprint("readers_api", __name__)


@readers_api.get("/readers")
@roles_required("administrador", "bibliotecario")
def readers():
    return jsonify(items=[user_json(person) for person in people(readers=True)])


@readers_api.post("/readers")
@roles_required("administrador")
def create_reader():
    payload = request.get_json(silent=True) or {}
    try:
        person = create_member(payload["name"], payload["email"], payload.get("documento_identidad"),
                               payload["role"], password_value(payload["password"]))
    except (ValueError, KeyError) as error:
        return jsonify(error=str(error)), 400
    return jsonify(user=user_json(person)), 201


@readers_api.patch("/readers/<int:reader_id>")
@roles_required("administrador")
def edit_reader(reader_id):
    payload = request.get_json(silent=True) or {}
    try:
        person = update_member(reader_id, payload.get("name"), payload.get("email"),
                               payload.get("documento_identidad"))
    except ValueError as error:
        return jsonify(error=str(error)), 400
    return jsonify(user=user_json(person))


@readers_api.delete("/readers/<int:reader_id>")
@roles_required("administrador")
def remove_reader(reader_id):
    try:
        delete_member(reader_id)
    except ValueError as error:
        return jsonify(error=str(error)), 400
    return jsonify(message="Lector eliminado")
