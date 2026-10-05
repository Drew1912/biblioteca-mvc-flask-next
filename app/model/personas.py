from main import db
from app.model.persona import Estudiante


def create_member(name: str, email: str) -> Estudiante:
    member = Estudiante(name=name.strip(), email=email.strip().lower())
    db.session.add(member)
    db.session.commit()
    return member


def get_member(member_id: int) -> Estudiante:
    member = db.session.get(Estudiante, member_id)
    if member is None:
        raise ValueError("Lector no encontrado")
    return member


def update_member(member_id: int, name: str | None, email: str | None) -> Estudiante:
    member = get_member(member_id)
    if name:
        member.name = name.strip()
    if email:
        member.email = email.strip().lower()
    db.session.commit()
    return member


def delete_member(member_id: int) -> None:
    member = get_member(member_id)
    if any(loan.returned_at is None for loan in member.loans):
        raise ValueError("No se puede eliminar un lector con préstamo activo")
    db.session.delete(member)
    db.session.commit()