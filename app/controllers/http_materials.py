from app.model import catalogo
from flask import Blueprint, jsonify, request

from app.controllers.http_security import login_required, roles_required
from app.view.serializers import material_json
from app.controllers.materiales import create_material, delete_material, update_material

materials_api = Blueprint("materials_api", __name__)


@materials_api.get("/materials")
@login_required
def materials():
    return jsonify({"items": [material_json(x) for x in catalogo.materials()]})


@materials_api.post("/materials")
@roles_required("administrador", "bibliotecario")
def create_material_api():
    payload = request.get_json(silent=True) or {}
    try:
        item = create_material(payload["type"], payload["title"], payload["isbn"], int(payload.get("copies", 1)))
    except (KeyError, ValueError) as error:
        return jsonify({"error": str(error)}), 400
    return jsonify({"item": material_json(item)}), 201


@materials_api.patch("/materials/<int:material_id>")
@roles_required("administrador", "bibliotecario")
def edit_material(material_id: int):
    payload = request.get_json(silent=True) or {}
    try:
        item = update_material(material_id, payload.get("title"), payload.get("isbn"))
    except (ValueError) as error:
        return jsonify({"error": str(error)}), 400
    return jsonify({"item": material_json(item)})


@materials_api.delete("/materials/<int:material_id>")
@roles_required("administrador", "bibliotecario")
def remove_material(material_id: int):
    try:
        delete_material(material_id)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify({"message": "Material eliminado"})
