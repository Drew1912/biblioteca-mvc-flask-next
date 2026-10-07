import pytest


def test_csrf_and_origin(client, account):
    account()
    payload = {"email": "administrador@test.local", "password": "Biblioteca123!"}
    assert client.post("/api/v1/auth/login", json=payload).status_code == 403
    assert client.post("/api/v1/auth/login", json=payload, headers={"X-CSRF-Token": "missing"}).status_code == 403
    token = client.get("/api/v1/auth/me").json["csrfToken"]
    headers = {"X-CSRF-Token": token, "Origin": "https://evil.example"}
    assert client.post("/api/v1/auth/login", json=payload, headers=headers).status_code == 403


def test_session_rotation_logout(session_client):
    client, headers, _ = session_client()
    assert client.get("/api/v1/auth/me").json["user"]["role"] == "administrador"
    assert client.post("/api/v1/auth/logout", headers=headers).status_code == 200
    assert client.get("/api/v1/materials").status_code == 401
    assert client.post("/api/v1/auth/logout", headers=headers).status_code == 403


@pytest.mark.parametrize("role", ["administrador", "bibliotecario", "docente", "estudiante"])
def test_permissions(session_client, role):
    client, headers, _ = session_client(role)
    manage = role in {"administrador", "bibliotecario"}
    assert client.get("/api/v1/materials").status_code == 200
    assert client.get("/api/v1/loans").status_code == 200
    assert client.get("/api/v1/users").status_code == (200 if manage else 403)
    assert client.get("/api/v1/reports/summary").status_code == (200 if manage else 403)
    response = client.post("/api/v1/materials", headers=headers,
                           json={"type": "libro", "title": "Prueba", "isbn": "TEST", "copies": 2})
    assert response.status_code == (201 if manage else 403)
    response = client.post("/api/v1/users", headers=headers, json={
        "name": "Nueva", "email": "nueva@test.local", "role": "docente", "password": "Biblioteca123!"})
    assert response.status_code == (201 if role == "administrador" else 403)


def test_cors(client):
    allowed = client.options("/api/v1/materials", headers={"Origin": "http://localhost:3000",
                             "Access-Control-Request-Method": "POST"})
    assert allowed.headers["Access-Control-Allow-Origin"] == "http://localhost:3000"
    assert allowed.headers["Access-Control-Allow-Credentials"] == "true"
    denied = client.get("/api/v1/health", headers={"Origin": "https://evil.example"})
    assert "Access-Control-Allow-Origin" not in denied.headers
    assert denied.headers["X-Content-Type-Options"] == "nosniff"


def test_rate_limit(client, account):
    account()
    token = client.get("/api/v1/auth/me").json["csrfToken"]
    for _ in range(10):
        assert client.post("/api/v1/auth/login", json={"email": "x", "password": "bad"},
                           headers={"X-CSRF-Token": token}).status_code == 401
    assert client.post("/api/v1/auth/login", json={}, headers={"X-CSRF-Token": token}).status_code == 429


def test_logout_with_empty_json_content_type(session_client):
    client, headers, _ = session_client()
    assert client.post("/api/v1/auth/logout", headers={**headers, "Content-Type": "application/json"}).status_code == 200


def test_write_requires_origin_even_with_csrf(client):
    token = client.get("/api/v1/auth/me").json["csrfToken"]
    response = client.post("/api/v1/auth/logout", headers={"X-CSRF-Token": token},
                           environ_overrides={"HTTP_ORIGIN": ""})
    assert response.status_code == 403
    assert response.json["error"] == "Origen no permitido"
