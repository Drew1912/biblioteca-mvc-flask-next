from main import db
from app.model.persona import (
    Administrador,
    Bibliotecario,
    Doctor,
    Estudiante,
    Persona,
)

ROLE_TYPES = {
    "administrador": Administrador,
    "bibliotecario": Bibliotecario,
    "doctor": Doctor,
    "estudiante": Estudiante,
}


def create_user(name: str, email: str, role: str, password: str | None = None) -> Persona:
    user_type = ROLE_TYPES.get(role.lower())
    if user_type is None:
        raise ValueError("Rol inválido")
    user = user_type(name=name.strip(), email=email.strip().lower())
    if password:
        user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def authenticate(email: str, password: str) -> Persona | None:
    user = Persona.query.filter_by(email=email.strip().lower(), active=True).first()
    return user if user and user.check_password(password) else None


def get_user(user_id: int) -> Persona:
    user = db.session.get(Persona, user_id)
    if user is None:
        raise ValueError("Usuario no encontrado")
    return user


def update_user(user_id: int, name: str | None, email: str | None) -> Persona:
    user = get_user(user_id)
    if name:
        user.name = name.strip()
    if email:
        user.email = email.strip().lower()
    db.session.commit()
    return user


def delete_user(user_id: int) -> None:
    user = get_user(user_id)
    if any(loan.returned_at is None for loan in user.loans):
        raise ValueError("No se puede eliminar un usuario con préstamo activo")
    db.session.delete(user)
    db.session.commit()