from app.main import db
from app.model.transaction import transactional
from app.model.validation import text


class Material(db.Model):
    __tablename__ = "material"

    id = db.Column(db.Integer, primary_key=True)
    tipo_material = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    total_copies = db.Column(db.Integer, nullable=False, default=1)
    available_copies = db.Column(db.Integer, nullable=False, default=1)
    issue_number = db.Column(db.String(30))
    university = db.Column(db.String(150))
    loans = db.relationship("Prestamo", back_populates="material")
    __mapper_args__ = {"polymorphic_on": tipo_material, "polymorphic_identity": "material"}

    @classmethod
    @transactional
    def create(cls, material_type: str, title: str, isbn: str, copies: int):
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

    @classmethod
    def get(cls, material_id: int):
        material = db.session.get(cls, material_id)
        if material is None:
            raise ValueError("Material no encontrado")
        return material

    def as_book(self):
        if not isinstance(self, Libro):
            raise ValueError("El material no es un libro")
        return self

    @transactional
    def update(self, title: str | None, isbn: str | None):
        if title is not None:
            self.title = text(title, "Título")
        if isbn is not None:
            self.isbn = text(isbn, "ISBN", 40)
        return self

    @transactional
    def delete(self) -> None:
        if self.loans:
            raise ValueError("No se puede eliminar un material con historial de préstamos")
        db.session.delete(self)


class Libro(Material):
    __mapper_args__ = {"polymorphic_identity": "libro"}


class Revista(Material):
    __mapper_args__ = {"polymorphic_identity": "revista"}


class Tesis(Material):
    __mapper_args__ = {"polymorphic_identity": "tesis"}


MATERIAL_TYPES = {"libro": Libro, "revista": Revista, "tesis": Tesis}
