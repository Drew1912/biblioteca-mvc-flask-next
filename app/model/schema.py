from sqlalchemy import inspect, text
from app.main import db


def initialize_database():
    """Crea tablas y aplica la transición aditiva de consola a web."""
    db.create_all()
    columns = {column["name"] for column in inspect(db.engine).get_columns("persona")}
    if "password_hash" not in columns:
        with db.engine.begin() as connection:
            connection.execute(text("ALTER TABLE persona ADD COLUMN password_hash VARCHAR(255)"))
