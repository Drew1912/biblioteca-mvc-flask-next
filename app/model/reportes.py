from datetime import UTC, datetime

from sqlalchemy import func

from app.model.material import Material
from app.model.persona import Persona
from app.model.prestamo import Prestamo


def summary() -> dict[str, int]:
    return {
        "materiales": Material.query.count(),
        "copias_disponibles": int(
            Material.query.with_entities(func.coalesce(func.sum(Material.available_copies), 0)).scalar()
        ),
        "usuarios": Persona.query.count(),
        "prestamos_activos": Prestamo.query.filter_by(returned_at=None).count(),
        "prestamos_vencidos": Prestamo.query.filter(
            Prestamo.returned_at.is_(None), Prestamo.due_at < datetime.now(UTC)
        ).count(),
    }


def inventory_rows() -> list[tuple[object, ...]]:
    return [
        (item.tipo_material, item.title, item.isbn, item.total_copies, item.available_copies)
        for item in Material.query.order_by(Material.tipo_material, Material.title).all()
    ]


def users_by_role_rows() -> list[tuple[object, ...]]:
    return [
        (user.tipo_persona, user.name, user.email, "Activo" if user.active else "Inactivo")
        for user in Persona.query.order_by(Persona.tipo_persona, Persona.name).all()
    ]


def loans_rows() -> list[tuple[object, ...]]:
    return [
        (loan.material.title, loan.persona.name, loan.due_at.strftime("%Y-%m-%d"),
         "Devuelto" if loan.returned_at else "Activo")
        for loan in Prestamo.query.order_by(Prestamo.due_at).all()
    ]


def overdue_rows() -> list[tuple[object, ...]]:
    now = datetime.now(UTC)
    return [
        (loan.material.title, loan.persona.name, loan.due_at.strftime("%Y-%m-%d"),
         (now - loan.due_at).days)
        for loan in Prestamo.query.filter(
            Prestamo.returned_at.is_(None), Prestamo.due_at < now
        ).order_by(Prestamo.due_at).all()
    ]