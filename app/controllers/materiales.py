from app.model.material import Libro, Material


def create_material(material_type: str, title: str, isbn: str, copies: int) -> Material:
    return Material.create(material_type, title, isbn, copies)


def create_book(title: str, isbn: str, copies: int) -> Libro:
    return create_material("libro", title, isbn, copies)


def get_material(material_id: int) -> Material:
    return Material.get(material_id)


def get_book(book_id: int) -> Libro:
    return get_material(book_id).as_book()


def update_material(material_id: int, title: str | None, isbn: str | None) -> Material:
    material = get_material(material_id)
    return material.update(title, isbn)


def update_book(book_id, title, isbn):
    return update_material(book_id, title, isbn)


def delete_material(material_id: int) -> None:
    material = get_material(material_id)
    material.delete()


def delete_book(book_id):
    delete_material(book_id)
