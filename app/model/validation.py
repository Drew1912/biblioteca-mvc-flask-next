import re


def text(value, label: str, limit: int = 120) -> str:
    if not isinstance(value, str) or not value.strip() or len(value.strip()) > limit:
        raise ValueError(f"{label}: introduce entre 1 y {limit} caracteres")
    return value.strip()


def email_address(value) -> str:
    value = text(value, "Correo", 254).lower()
    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", value):
        raise ValueError("Correo inválido")
    return value


def password_value(value) -> str:
    if not isinstance(value, str) or not 12 <= len(value) <= 128:
        raise ValueError("La contraseña debe tener entre 12 y 128 caracteres")
    return value
