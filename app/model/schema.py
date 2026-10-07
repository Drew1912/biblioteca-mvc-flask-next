from sqlalchemy import inspect, text
from app.main import db


def initialize_database():
    """Actualiza bases anteriores sin eliminar cuentas ni historial."""
    db.create_all()
    columns = {column["name"] for column in inspect(db.engine).get_columns("persona")}
    additions = {"password_hash": "VARCHAR(255)", "carnet_identidad": "VARCHAR(20)",
                 "biblioteca_id": "INTEGER REFERENCES bibliotecas(id)"}
    with db.engine.begin() as connection:
        for name, definition in additions.items():
            if name not in columns:
                connection.execute(text(f"ALTER TABLE persona ADD COLUMN {name} {definition}"))
        connection.execute(text("UPDATE persona SET tipo_persona = 'docente' WHERE tipo_persona = 'doctor'"))
        if "carnet_identidad" not in columns:
            connection.execute(text("UPDATE persona SET carnet_identidad = 'LEGACY-' || CAST(id AS VARCHAR)"))
            connection.execute(text("CREATE UNIQUE INDEX uq_persona_carnet ON persona (carnet_identidad)"))
