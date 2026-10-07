from app.model.persona import Persona


def create_user(name: str, email: str, role: str, password: str | None = None,
                documento_identidad: str | None = None) -> Persona:
    return Persona.create(name, email, role, password, documento_identidad)


def authenticate(email: str, password: str) -> Persona | None:
    return Persona.authenticate(email, password)


def get_user(user_id: int) -> Persona:
    return Persona.get(user_id)


def update_user(user_id: int, name: str | None = None, email: str | None = None,
                documento_identidad: str | None = None) -> Persona:
    user = get_user(user_id)
    return user.update(name, email, documento_identidad)


def delete_user(user_id: int) -> None:
    user = get_user(user_id)
    user.delete()


def active_user(user_id):
    return Persona.active_user(user_id)


def set_user_password(user_id, password):
    user = get_user(user_id)
    user.change_password(password)
