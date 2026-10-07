import pytest

from app.main import db
from app.model.material import Libro
from app.model.persona import Estudiante
from app.controllers.materiales import create_book, delete_book, update_book
from app.controllers.personas import create_member
from app.controllers.prestamos import checkout_book, return_book
from app.model.reportes import summary
from app.model.seed import seed_database
from app.controllers.usuarios import create_user


def test_checkout_and_return_restore_availability(app):
    with app.app_context():
        book = create_book("Dune", "9780441172719", 1)
        member = create_member("Ana", "ANA@example.com")

        loan = checkout_book(book.id, member.id, 14)
        assert loan.book.available_copies == 0

        return_book(loan.id)
        assert db.session.get(Libro, book.id).available_copies == 1


def test_uml_inheritance_uses_material_and_persona_subclasses(app):
    with app.app_context():
        book = create_book("Dune", "9780441172719", 1)
        member = create_member("Ana", "ana@example.com")

        assert isinstance(book, Libro)
        assert isinstance(member, Estudiante)
        assert book.tipo_material == "libro"
        assert member.tipo_persona == "estudiante"


def test_checkout_rejects_unavailable_book(app):
    with app.app_context():
        book = create_book("Dune", "9780441172719", 1)
        member = create_member("Ana", "ana@example.com")
        checkout_book(book.id, member.id, 14)

        with pytest.raises(ValueError, match="No hay copias"):
            checkout_book(book.id, member.id, 14)


def test_cli_creates_and_lists_books(app, runner):
    result = runner.invoke(
        args=["library", "materials", "create", "--type", "libro", "--title", "Dune", "--isbn", "9780441172719"]
    )
    assert result.exit_code == 0
    assert "Material creado: 1" in result.output

    result = runner.invoke(args=["library", "materials", "list"])
    assert result.exit_code == 0
    assert "Dune" in result.output


def test_duplicate_member_email_is_reported(app, runner):
    first = runner.invoke(
        args=["library", "readers", "create", "--name", "Ana", "--email", "ana@example.com"]
    )
    second = runner.invoke(
        args=["library", "readers", "create", "--name", "Otra", "--email", "ANA@example.com"]
    )
    assert first.exit_code == 0
    assert second.exit_code != 0
    assert "email ya está registrado" in second.output


def test_book_update_and_delete_crud(app):
    with app.app_context():
        book = create_book("Dune", "9780441172719", 1)

        update_book(book.id, "Dune actualizado", None)
        assert db.session.get(Libro, book.id).title == "Dune actualizado"

        delete_book(book.id)
        assert db.session.get(Libro, book.id) is None


def test_users_and_reports(app):
    with app.app_context():
        create_user("Berta", "berta@example.com", "bibliotecario")
        book = create_book("Dune", "9780441172719", 2)
        member = create_member("Ana", "ana@example.com")
        checkout_book(book.id, member.id, 14)

        report = summary()
        assert report["usuarios"] == 2
        assert report["materiales"] == 1
        assert report["copias_disponibles"] == 1
        assert report["prestamos_activos"] == 1


def test_seed_creates_minimum_dataset(app):
    with app.app_context():
        counts = seed_database(reset=True)

        assert counts == {"materiales": 20, "personas": 40, "prestamos": 20}
        assert summary()["copias_disponibles"] == 40