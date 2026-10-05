from app.model.transaction import transactional
from app.main import db
from app.model.validation import text, email_address, password_value
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


@transactional
def create_user(name: str, email: str, role: str, password: str | None = None) -> Persona:
    user_type = ROLE_TYPES.get(text(role, "Rol").lower())
    if user_type is None:
        raise ValueError("Rol inválido")
    user = user_type(name=text(name, "Nombre"), email=email_address(email))
    if password:
        user.set_password(password_value(password))
    db.session.add(user)
    return user


def authenticate(email: str, password: str) -> Persona | None:
    user = Persona.query.filter_by(email=email.strip().lower(), active=True).first()
    return user if user and user.check_password(password) else None


def get_user(user_id: int) -> Persona:
    user = db.session.get(Persona, user_id)
    if user is None:
        raise ValueError("Usuario no encontrado")
    return user


@transactional
def update_user(user_id: int, name: str | None, email: str | None) -> Persona:
    user = get_user(user_id)
    if name is not None:
        user.name = text(name, "Nombre")
    if email is not None:
        user.email = email_address(email)
    return user


@transactional
def delete_user(user_id: int) -> None:
    user = get_user(user_id)
    if user.loans:
        raise ValueError("No se puede eliminar un usuario con historial de préstamos")
    db.session.delete(user)


def active_user(user_id):
    user = db.session.get(Persona, user_id) if user_id else None
    return user if user and user.active else None


@transactional
def set_user_password(user_id, password):
    user = get_user(user_id)
    user.set_password(password_value(password))
