from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError

from main import db
from app.api.security import current_user, login_required, roles_required
from app.api.serializers import loan_json, material_json, user_json
from app.model.material import Material
from app.model.materiales import create_material, delete_material, update_material
from app.model.persona import Persona
from app.model.prestamo import Prestamo
from app.model.prestamos import checkout_book, return_book
from app.model.reportes import inventory_rows, loans_rows, overdue_rows, summary, users_by_role_rows
from app.model.usuarios import create_user, delete_user, update_user

resources_api = Blueprint("resources_api", __name__)


@resources_api.get("/health")
def health():
    return jsonify({"status": "ok"})


@resources_api.get("/materials")
@login_required
def materials():
    return jsonify({"items": [material_json(x) for x in Material.query.order_by(Material.title).all()]})


@resources_api.post("/materials")
@roles_required("administrador", "bibliotecario")
def create_material_api():
    payload = request.get_json(silent=True) or {}
    try:
        item = create_material(payload["type"], payload["title"], payload["isbn"], int(payload.get("copies", 1)))
    except (KeyError, ValueError, IntegrityError) as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400
    return jsonify({"item": material_json(item)}), 201


@resources_api.patch("/materials/<int:material_id>")
@roles_required("administrador", "bibliotecario")
def edit_material(material_id: int):
    payload = request.get_json(silent=True) or {}
    try:
        item = update_material(material_id, payload.get("title"), payload.get("isbn"))
    except (ValueError, IntegrityError) as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400
    return jsonify({"item": material_json(item)})


@resources_api.delete("/materials/<int:material_id>")
@roles_required("administrador", "bibliotecario")
def remove_material(material_id: int):
    try:
        delete_material(material_id)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify({"message": "Material eliminado"})


@resources_api.get("/users")
@roles_required("administrador", "bibliotecario")
def users():
    return jsonify({"items": [user_json(x) for x in Persona.query.order_by(Persona.name).all()]})


@resources_api.post("/users")
@roles_required("administrador")
def create_user_api():
    payload = request.get_json(silent=True) or {}
    try:
        user = create_user(payload["name"], payload["email"], payload["role"], payload["password"])
    except (KeyError, ValueError, IntegrityError) as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400
    return jsonify({"user": user_json(user)}), 201


@resources_api.patch("/users/<int:user_id>")
@roles_required("administrador")
def edit_user(user_id: int):
    payload = request.get_json(silent=True) or {}
    try:
        user = update_user(user_id, payload.get("name"), payload.get("email"))
    except (ValueError, IntegrityError) as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400
    return jsonify({"user": user_json(user)})


@resources_api.delete("/users/<int:user_id>")
@roles_required("administrador")
def remove_user(user_id: int):
    try:
        delete_user(user_id)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify({"message": "Usuario eliminado"})


@resources_api.get("/loans")
@login_required
def loans():
    user = current_user()
    query = Prestamo.query if user.tipo_persona in {"administrador", "bibliotecario"} else Prestamo.query.filter_by(persona_id=user.id)
    return jsonify({"items": [loan_json(x) for x in query.order_by(Prestamo.due_at).all()]})


@resources_api.post("/loans")
@roles_required("administrador", "bibliotecario")
def create_loan_api():
    payload = request.get_json(silent=True) or {}
    try:
        loan = checkout_book(int(payload["materialId"]), int(payload["personId"]), int(payload.get("days", 14)))
    except (KeyError, ValueError) as error:
        return jsonify({"error": str(error)}), 400
    return jsonify({"loan": loan_json(loan)}), 201


@resources_api.post("/loans/<int:loan_id>/return")
@roles_required("administrador", "bibliotecario")
def return_loan_api(loan_id: int):
    try:
        loan = return_book(loan_id)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify({"loan": loan_json(loan)})


@resources_api.get("/reports/<string:report_type>")
@login_required
def report(report_type: str):
    if report_type == "summary":
        return jsonify(summary())
    if current_user().tipo_persona not in {"administrador", "bibliotecario"}:
        return jsonify({"error": "Permisos insuficientes"}), 403
    data = {"inventory": inventory_rows, "users": users_by_role_rows, "loans": loans_rows, "overdue": overdue_rows}.get(report_type)
    if data is None:
        return jsonify({"error": "Reporte no encontrado"}), 404
    return jsonify({"items": data()})
