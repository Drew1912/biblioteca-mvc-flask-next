from functools import wraps
from typing import Callable

from flask import jsonify, session

from main import db
from app.model.persona import Persona


def current_user() -> Persona | None:
    user_id = session.get("user_id")
    return db.session.get(Persona, user_id) if user_id else None


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
