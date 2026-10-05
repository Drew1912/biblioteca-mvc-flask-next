from flask import Blueprint, jsonify

from app.controllers.http_security import current_user, login_required
from app.model.reportes import inventory_rows, loans_rows, overdue_rows, summary, users_by_role_rows

reports_api = Blueprint("reports_api", __name__)


@reports_api.get("/reports/<string:report_type>")
@login_required
def report(report_type: str):
    if current_user().tipo_persona not in {"administrador", "bibliotecario"}:
        return jsonify({"error": "Permisos insuficientes"}), 403
    if report_type == "summary":
        return jsonify(summary())
    data = {"inventory": inventory_rows, "users": users_by_role_rows, "loans": loans_rows, "overdue": overdue_rows}.get(report_type)
    if data is None:
        return jsonify({"error": "Reporte no encontrado"}), 404
    return jsonify({"items": data()})
