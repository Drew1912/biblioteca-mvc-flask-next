from app.model.material import Material
from app.model.persona import Persona
from app.model.prestamo import Prestamo


def material_json(item: Material) -> dict:
    return {
        "id": item.id,
        "type": item.tipo_material,
        "title": item.title,
        "isbn": item.isbn,
        "totalCopies": item.total_copies,
        "availableCopies": item.available_copies,
    }


def user_json(user: Persona) -> dict:
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "carnetIdentity": user.carnet_identidad,
        "role": user.tipo_persona,
        "active": user.active,
    }


def loan_json(loan: Prestamo) -> dict:
    return {
        "id": loan.id,
        "material": material_json(loan.material),
        "user": user_json(loan.persona),
        "loanedAt": loan.loaned_at.isoformat(),
        "dueAt": loan.due_at.isoformat(),
        "returnedAt": loan.returned_at.isoformat() if loan.returned_at else None,
    }
