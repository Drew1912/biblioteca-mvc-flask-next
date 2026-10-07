from concurrent.futures import ThreadPoolExecutor
import pytest
from app.main import db
from app.controllers.materiales import create_book
from app.controllers.usuarios import create_user
from app.controllers.prestamos import checkout_book, return_book
from app.model.material import Material


def test_concurrent_checkout_and_return(app):
    if db.engine.dialect.name != "postgresql":
        pytest.skip("Los bloqueos de filas requieren TEST_DATABASE_URL PostgreSQL")
    book = create_book("Concurrencia", "THREAD", 1)
    person = create_user("Concurrente", "concurrent@test.local", "estudiante")
    book_id, person_id = book.id, person.id

    def checkout(_):
        with app.app_context():
            try:
                return checkout_book(book_id, person_id, 7).id
            except ValueError:
                return None
            finally:
                db.session.remove()

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(checkout, range(2)))
    assert sum(result is not None for result in results) == 1
    loan_id = next(result for result in results if result is not None)

    def checkin(_):
        with app.app_context():
            try:
                return_book(loan_id)
                return True
            except ValueError:
                return False
            finally:
                db.session.remove()

    with ThreadPoolExecutor(max_workers=2) as pool:
        assert sorted(pool.map(checkin, range(2))) == [False, True]
    db.session.expire_all()
    assert db.session.get(Material, book_id).available_copies == 1
