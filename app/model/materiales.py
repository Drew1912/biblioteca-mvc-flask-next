from app.model.transaction import transactional
from app.model import db
from app.model.validation import text
from app.model.material import Libro, Material, Revista, Tesis

MATERIAL_TYPES = {"libro": Libro, "revista": Revista, "tesis": Tesis}


@transactional
def create_material(material_type: str, title: str, isbn: str, copies: int) -> Material:
    material_class = MATERIAL_TYPES.get(text(material_type, "Tipo").lower())
    if material_class is None:
        raise ValueError("Tipo de material inválido")
    if copies < 1:
        raise ValueError("Las copias deben ser mayores que cero")
    material = material_class(
        title=text(title, "Título"),
        isbn=text(isbn, "ISBN", 40),
        total_copies=copies,
        available_copies=copies,
    )
    db.session.add(material)
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


def update_book(book_id, title, isbn):
    return update_material(book_id, title, isbn)


@transactional
def update_material(material_id: int, title: str | None, isbn: str | None) -> Material:
    material = get_material(material_id)
    if title is not None:
        material.title = text(title, "Título")
    if isbn is not None:
        material.isbn = text(isbn, "ISBN", 40)
    return material


def delete_book(book_id):
    delete_material(book_id)


@transactional
def delete_material(material_id: int) -> None:
    material = get_material(material_id)
    if material.loans:
        raise ValueError("No se puede eliminar un material con historial de préstamos")
    db.session.delete(material)
