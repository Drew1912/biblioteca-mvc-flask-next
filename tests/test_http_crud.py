import pytest


def test_material_crud_and_rollback(session_client):
    client, headers, _ = session_client()
    payload = {"type": "libro", "title": "Original", "isbn": "UNIQUE", "copies": 2}
    created = client.post("/api/v1/materials", json=payload, headers=headers)
    assert created.status_code == 201
    path = f"/api/v1/materials/{created.json['item']['id']}"
    assert client.post("/api/v1/materials", json=payload, headers=headers).status_code == 409
    edited = client.patch(path, json={"title": "Editado"}, headers=headers)
    assert edited.json["item"]["title"] == "Editado"
    assert client.delete(path, headers=headers).status_code == 200
    assert client.get("/api/v1/materials").json["items"] == []


@pytest.mark.parametrize("payload", [[], None, {"type": None},
                         {"type": "libro", "title": "", "isbn": "X"},
                         {"type": "libro", "title": "X", "isbn": "X", "copies": -1}])
def test_invalid_payload(session_client, payload):
    client, headers, _ = session_client()
    assert client.post("/api/v1/materials", json=payload, headers=headers).status_code == 400


def test_users_crud(session_client):
    client, headers, own_id = session_client()
    response = client.post("/api/v1/users", headers=headers, json={"name": "Nueva", "email": "new@test.local",
                           "role": "estudiante", "password": "Biblioteca123!"})
    assert response.status_code == 201
    assert "password" not in str(response.json)
    path = f"/api/v1/users/{response.json['user']['id']}"
    assert client.patch(path, json={"name": "Editada"}, headers=headers).json["user"]["name"] == "Editada"
    assert client.delete(path, headers=headers).status_code == 200
    assert client.delete(f"/api/v1/users/{own_id}", headers=headers).status_code == 400


def test_loan_lifecycle(session_client, account):
    client, headers, _ = session_client()
    reader = account("estudiante")
    material = client.post("/api/v1/materials", headers=headers,
                           json={"type": "libro", "title": "Único", "isbn": "X", "copies": 1}).json["item"]
    payload = {"materialId": material["id"], "personId": reader, "days": 14}
    response = client.post("/api/v1/loans", json=payload, headers=headers)
    assert response.status_code == 201
    assert client.post("/api/v1/loans", json=payload, headers=headers).status_code == 400
    path = f"/api/v1/loans/{response.json['loan']['id']}/return"
    assert client.post(path, headers=headers).status_code == 200
    assert client.post(path, headers=headers).status_code == 400
    assert client.get("/api/v1/materials").json["items"][0]["availableCopies"] == 1
    assert client.delete(f"/api/v1/materials/{material['id']}", headers=headers).status_code == 400
    for report in ["summary", "inventory", "users", "loans", "overdue"]:
        assert client.get(f"/api/v1/reports/{report}").status_code == 200


def test_reader_only_sees_own_loans(app, session_client, account):
    from app.model.materiales import create_book
    from app.model.prestamos import checkout_book
    client, _, own_id = session_client("estudiante")
    other_id = account("doctor")
    with app.app_context():
        book = create_book("Privacidad", "P", 2)
        checkout_book(book.id, own_id, 7)
        checkout_book(book.id, other_id, 7)
    items = client.get("/api/v1/loans").json["items"]
    assert len(items) == 1
    assert items[0]["user"]["id"] == own_id
