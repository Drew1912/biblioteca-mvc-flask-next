import pytest

from app.main import db
from app.model.catalogo import people
from app.controllers.materiales import create_book
from app.model.persona import Docente, Persona
from app.controllers.prestamos import checkout_book
from app.model.seed import seed_database
from app.controllers.usuarios import create_user


def test_readers_crud_and_group_reports(session_client):
    client, headers, _ = session_client()
    payload = {"name": "Docente", "email": "prof@test.local", "role": "docente",
               "password": "Biblioteca123!", "documento_identidad": "CI-123"}
    response = client.post("/api/v1/readers", json=payload, headers=headers)
    assert response.status_code == 201
    reader = response.json["user"]
    path = f"/api/v1/readers/{reader['id']}"
    assert client.patch(path, json={"name": "Profesora"}, headers=headers).status_code == 200
    assert [x["role"] for x in client.get("/api/v1/readers").json["items"]] == ["docente"]
    assert [x["role"] for x in client.get("/api/v1/users?group=staff").json["items"]] == ["administrador"]
    assert client.get("/api/v1/reports/readers").json["items"][0][:2] == ["docente", "Profesora"]
    assert client.get("/api/v1/reports/users").json["items"][0][0] == "administrador"
    assert client.delete(path, headers=headers).status_code == 200
    assert not client.get("/api/v1/readers").json["items"]


@pytest.mark.parametrize("role", ["administrador", "bibliotecario", "docente", "estudiante"])
def test_reader_permissions(session_client, account, role):
    client, headers, _ = session_client(role)
    reader = account("estudiante", "another@test.local")
    path = f"/api/v1/readers/{reader}"
    manager = role in {"administrador", "bibliotecario"}
    assert client.get("/api/v1/readers").status_code == (200 if manager else 403)
    assert client.get("/api/v1/reports/readers").status_code == (200 if manager else 403)
    assert client.patch(path, json={"name": "Cambio"}, headers=headers).status_code == (200 if role == "administrador" else 403)
    assert client.delete(path, headers=headers).status_code == (200 if role == "administrador" else 403)


def test_reader_history_and_staff_cannot_be_deleted_as_reader(app, session_client, account):
    client, headers, admin = session_client()
    reader = account("docente")
    with app.app_context():
        book = create_book("Historia", "HIST", 1)
        checkout_book(book.id, reader, 14)
    assert client.delete(f"/api/v1/readers/{reader}", headers=headers).status_code == 400
    assert client.delete(f"/api/v1/readers/{admin}", headers=headers).status_code == 400


@pytest.mark.parametrize("role", ["doctor", "persona", "otro"])
def test_removed_or_unknown_role_rejected(session_client, role):
    client, headers, _ = session_client()
    payload = {"name": "Inválido", "email": "bad@test.local", "role": role, "password": "Biblioteca123!"}
    assert client.post("/api/v1/users", json=payload, headers=headers).status_code == 400
    assert client.post("/api/v1/readers", json=payload, headers=headers).status_code == 400


def test_seed_has_internal_users_and_both_reader_roles(app):
    with app.app_context():
        seed_database()
        assert len(people(staff=True)) == 20
        assert len(people(readers=True)) == 20
        assert {x.tipo_persona for x in people()} == {"administrador", "bibliotecario", "docente", "estudiante"}
        assert isinstance(Persona.query.filter_by(email="lector02@test.local").one(), Docente)


@pytest.mark.parametrize("role", ["docente", "estudiante"])
def test_readers_cannot_mutate_loans_and_see_only_their_history(app, session_client, account, role):
    client, headers, own_id = session_client(role)
    other_id = account("estudiante", "other@test.local")
    with app.app_context():
        book = create_book("Privado", "PRIV", 2)
        own = checkout_book(book.id, own_id, 7).id
        checkout_book(book.id, other_id, 7)
        material_id = book.id
    assert {x["user"]["id"] for x in client.get("/api/v1/loans").json["items"]} == {own_id}
    payload = {"materialId": material_id, "personId": other_id}
    assert client.post("/api/v1/loans", json=payload, headers=headers).status_code == 403
    assert client.post(f"/api/v1/loans/{own}/return", headers=headers).status_code == 403
    with app.app_context():
        assert db.session.get(Persona, own_id).loans[0].returned_at is None


def test_identity_length_is_validated(app):
    with app.app_context(), pytest.raises(ValueError, match="20 caracteres"):
        create_user("Persona", "identity@test.local", "estudiante", documento_identidad="X" * 21)
