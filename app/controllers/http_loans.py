from app.model import catalogo
from flask import Blueprint, jsonify, request

from app.controllers.http_security import current_user, login_required, roles_required
from app.view.serializers import loan_json
from app.model.prestamos import checkout_book, return_book

loans_api = Blueprint("loans_api", __name__)


@loans_api.get("/loans")
@login_required
def loans():
    user = current_user()
    return jsonify({"items": [loan_json(x) for x in catalogo.loans(user)]})


@loans_api.post("/loans")
@roles_required("administrador", "bibliotecario")
def create_loan_api():
    payload = request.get_json(silent=True) or {}
    try:
        loan = checkout_book(int(payload["materialId"]), int(payload["personId"]), int(payload.get("days", 14)))
    except (KeyError, ValueError) as error:
        return jsonify({"error": str(error)}), 400
    return jsonify({"loan": loan_json(loan)}), 201


@loans_api.post("/loans/<int:loan_id>/return")
@roles_required("administrador", "bibliotecario")
def return_loan_api(loan_id: int):
    try:
        loan = return_book(loan_id)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify({"loan": loan_json(loan)})
