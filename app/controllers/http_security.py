from functools import wraps
from typing import Callable

from flask import jsonify, session

from app.model.usuarios import active_user
from app.model.persona import Persona


def current_user() -> Persona | None:
    return active_user(session.get("user_id"))


def login_required(view: Callable):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if current_user() is None:
            return jsonify({"error": "Autenticación requerida"}), 401
        return view(*args, **kwargs)
    return wrapped


def roles_required(*roles: str):
    def decorator(view: Callable):
        @wraps(view)
        @login_required
        def wrapped(*args, **kwargs):
            user = current_user()
            if user.tipo_persona not in roles:
                return jsonify({"error": "Permisos insuficientes"}), 403
            return view(*args, **kwargs)
        return wrapped
    return decorator
