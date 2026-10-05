from sqlalchemy import text, inspect
from app.main import db
from app.model.schema import initialize_database


def test_add_password_column_preserves_people(app):
    with app.app_context():
        db.drop_all()
        with db.engine.begin() as connection:
            connection.execute(text("CREATE TABLE persona (id INTEGER PRIMARY KEY, tipo_persona VARCHAR(30), "
                                    "name VARCHAR(120), email VARCHAR(254), active BOOLEAN)"))
            connection.execute(text("INSERT INTO persona VALUES (1, 'estudiante', 'Anterior', 'old@test.local', TRUE)"))
        initialize_database()
        initialize_database()
        assert "password_hash" in {c["name"] for c in inspect(db.engine).get_columns("persona")}
        assert db.session.execute(text("SELECT name, password_hash FROM persona")).one() == ("Anterior", None)
