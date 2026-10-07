import os
import pytest

from app import create_app
from app.main import db


@pytest.fixture()
def app(tmp_path):
    database = os.getenv("TEST_DATABASE_URL", f"sqlite:///{tmp_path / 'test.db'}")
    if not database.startswith("sqlite:") and not database.endswith("/biblioteca_test"):
        raise ValueError("Las pruebas PostgreSQL requieren una base aislada biblioteca_test")
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": database,
        }
    )
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def client(app):
    client = app.test_client()
    client.environ_base["HTTP_ORIGIN"] = app.config["WEB_ORIGIN"]
    return client

@pytest.fixture()
def account(app):
    from app.controllers.usuarios import create_user

    def create(role="administrador", email=None):
        with app.app_context():
            return create_user("Persona ficticia", email or f"{role}@test.local", role, "Biblioteca123!").id
    return create


@pytest.fixture()
def session_client(client, account):
    def start(role="administrador"):
        user_id = account(role)
        token = client.get("/api/v1/auth/me").json["csrfToken"]
        response = client.post("/api/v1/auth/login", json={
            "email": f"{role}@test.local", "password": "Biblioteca123!"
        }, headers={"X-CSRF-Token": token})
        assert response.status_code == 200
        return client, {"X-CSRF-Token": response.json["csrfToken"]}, user_id
    return start
