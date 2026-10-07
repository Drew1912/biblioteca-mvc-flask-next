from app.model.transaction import transactional
from flask import current_app
from datetime import UTC, datetime, timedelta

from app.model import db
from app.model.material import Libro, Material, Revista, Tesis
from app.model.persona import Administrador, Bibliotecario, Doctor, Estudiante, Persona
from app.model.prestamo import Prestamo


MATERIAL_TYPES = (Libro, Revista, Tesis)
USER_TYPES = (Administrador, Bibliotecario, Doctor)


@transactional
def seed_database(reset: bool = False) -> dict[str, int]:
    if current_app.config["APP_ENV"] == "production":
        raise ValueError("Semilla deshabilitada en producción")
    if reset:
        _clear_database()
    elif Material.query.count() or Persona.query.count() or Prestamo.query.count():
        _development_passwords()
        return _counts()

    materials = [
        material_type(
            title=f"Material de prueba {index:02d}",
            isbn=f"TEST-{index:04d}",
            total_copies=3,
            available_copies=2,
        )
        for index, material_type in ((index, MATERIAL_TYPES[index % 3]) for index in range(1, 21))
    ]
    students = [
        Estudiante(name=f"Lector de prueba {index:02d}", carnet_identidad=f"LECTOR-{index:02d}",
                   email=f"lector{index:02d}@test.local")
        for index in range(1, 21)
    ]
    staff = [
        user_type(name=f"Usuario de prueba {index:02d}", carnet_identidad=f"USUARIO-{index:02d}",
                  email=f"usuario{index:02d}@test.local")
        for index, user_type in ((index, USER_TYPES[index % 3]) for index in range(1, 21))
    ]
    db.session.add_all(materials + students + staff)
    db.session.flush()
    for user in students + staff:
        user.set_password("Biblioteca123!")

    loans = [
        Prestamo(
            material=materials[index - 1],
            persona=students[index - 1],
            loaned_at=datetime.now(UTC) - timedelta(days=index),
            due_at=datetime.now(UTC) + timedelta(days=14 - index),
        )
        for index in range(1, 21)
    ]
    db.session.add_all(loans)
    return _counts()


def _clear_database() -> None:
    db.session.query(Prestamo).delete()
    db.session.query(Material).delete()
    db.session.query(Persona).delete()


def _counts() -> dict[str, int]:
    return {
        "materiales": Material.query.count(),
        "personas": Persona.query.count(),
        "prestamos": Prestamo.query.count(),
    }


def _development_passwords():
    for prefix, name in (("lector", "Lector de prueba"), ("usuario", "Usuario de prueba")):
        for index in range(1, 21):
            person = Persona.query.filter_by(email=f"{prefix}{index:02d}@test.local",
                                             name=f"{name} {index:02d}").first()
            if person and not person.password_hash:
                person.set_password("Biblioteca123!")
