from main import db
from app.model.material import Libro, Material, Revista, Tesis

MATERIAL_TYPES = {"libro": Libro, "revista": Revista, "tesis": Tesis}


def create_material(material_type: str, title: str, isbn: str, copies: int) -> Material:
    material_class = MATERIAL_TYPES.get(material_type.lower())
    if material_class is None:
        raise ValueError("Tipo de material inválido")
    if copies < 1:
        raise ValueError("Las copias deben ser mayores que cero")
    material = material_class(
        title=title.strip(),
        isbn=isbn.strip(),
        total_copies=copies,
        available_copies=copies,
    )
    db.session.add(material)
    db.session.commit()
    return material


def create_book(title: str, isbn: str, copies: int) -> Libro:
    return create_material("libro", title, isbn, copies)


def get_material(material_id: int) -> Material:
    material = db.session.get(Material, material_id)
    if material is None:
        raise ValueError("Material no encontrado")
    return material


def get_book(book_id: int) -> Libro:
    material = get_material(book_id)
    if not isinstance(material, Libro):
        raise ValueError("El material no es un libro")
    return material


def update_book(book_id: int, title: str | None, isbn: str | None) -> Libro:
    book = get_material(book_id)
    if title:
        book.title = title.strip()
    if isbn:
        book.isbn = isbn.strip()
    db.session.commit()
    return book


def update_material(material_id: int, title: str | None, isbn: str | None) -> Material:
    material = get_material(material_id)
    if title:
        material.title = title.strip()
    if isbn:
        material.isbn = isbn.strip()
    db.session.commit()
    return material


def delete_book(book_id: int) -> None:
    material = get_material(book_id)
    if any(loan.returned_at is None for loan in material.loans):
        raise ValueError("No se puede eliminar un libro con préstamo activo")
    db.session.delete(material)
    db.session.commit()


def delete_material(material_id: int) -> None:
    material = get_material(material_id)
    if any(loan.returned_at is None for loan in material.loans):
        raise ValueError("No se puede eliminar un material con préstamo activo")
    db.session.delete(material)
    db.session.commit()