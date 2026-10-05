def login(client, email="usuario03@test.local", password="Biblioteca123!"):
    token = client.get("/api/v1/auth/me").json["csrfToken"]
    return client.post("/api/v1/auth/login", json={"email": email, "password": password},
                       headers={"X-CSRF-Token": token})


def test_health_is_public(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"


def test_login_and_materials_require_session(app, client):
    with app.app_context():
        from app.model.seed import seed_database
        seed_database(reset=True)

    assert client.get("/api/v1/materials").status_code == 401
    response = login(client)
    assert response.status_code == 200
    assert response.json["user"]["role"] == "administrador"
    assert client.get("/api/v1/materials").status_code == 200


def test_student_cannot_manage_materials(app, client):
    with app.app_context():
        from app.model.seed import seed_database
        seed_database(reset=True)

    response = login(client, "lector01@test.local", "Biblioteca123!")
    assert response.status_code == 200
    assert response.json["user"]["role"] == "estudiante"
    assert client.post("/api/v1/materials", json={"type": "libro", "title": "No", "isbn": "NO", "copies": 1}).status_code == 403
