from datetime import UTC, datetime, timedelta

from main import db
from app.model.material import Material
from app.model.persona import Persona
from app.model.prestamo import Prestamo


def checkout_book(book_id: int, member_id: int, days: int) -> Prestamo:
    book = db.session.get(Material, book_id)
    member = db.session.get(Persona, member_id)
    if book is None:
        raise ValueError("Material no encontrado")
    if member is None or not member.active:
        raise ValueError("Lector no encontrado o inactivo")
    if book.available_copies < 1:
        raise ValueError("No hay copias disponibles")
    if days < 1:
        raise ValueError("Los días deben ser mayores que cero")

    book.available_copies -= 1
    loan = Prestamo(
        material=book,
        persona=member,
        due_at=datetime.now(UTC) + timedelta(days=days),
    )
    db.session.add(loan)
    db.session.commit()
    return loan


def get_loan(loan_id: int) -> Prestamo:
    loan = db.session.get(Prestamo, loan_id)
    if loan is None:
        raise ValueError("Préstamo no encontrado")
    return loan


def return_book(loan_id: int) -> Prestamo:
    loan = get_loan(loan_id)
    if loan.returned_at is not None:
        raise ValueError("El préstamo ya fue devuelto")
    loan.returned_at = datetime.now(UTC)
    loan.material.available_copies += 1
    db.session.commit()
    return loan


def delete_loan(loan_id: int) -> None:
    loan = get_loan(loan_id)
    if loan.returned_at is None:
        loan.material.available_copies += 1
    db.session.delete(loan)
    db.session.commit()