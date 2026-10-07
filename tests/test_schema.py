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


def test_legacy_role_migrates_without_losing_login_or_loans(app):
    from app.controllers.materiales import create_book
    from app.model.persona import Docente, Persona
    from app.controllers.prestamos import checkout_book
    from app.controllers.usuarios import create_user
    with app.app_context():
        person = create_user("Anterior", "legacy@test.local", "docente", "Biblioteca123!")
        person_id = person.id
        book = create_book("Historial", "LEGACY", 1)
        loan_id = checkout_book(book.id, person.id, 7).id
        db.session.execute(text("UPDATE persona SET tipo_persona = 'doctor' WHERE id = :id"), {"id": person_id})
        db.session.commit()
        db.session.remove()
        initialize_database()
        initialize_database()
        migrated = db.session.get(Persona, person_id)
        assert isinstance(migrated, Docente)
        assert migrated.check_password("Biblioteca123!")
        assert [loan.id for loan in migrated.loans] == [loan_id]
