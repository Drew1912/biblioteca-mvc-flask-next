from app.model.prestamo import Prestamo


def checkout_book(book_id: int, member_id: int, days: int) -> Prestamo:
    return Prestamo.checkout(book_id, member_id, days)


def get_loan(loan_id: int) -> Prestamo:
    return Prestamo.get(loan_id)


def return_book(loan_id: int) -> Prestamo:
    return Prestamo.return_material(loan_id)


def delete_loan(loan_id: int) -> None:
    loan = get_loan(loan_id)
    loan.delete()
