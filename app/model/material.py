from app.model import db


class Material(db.Model):
    __tablename__ = "material"
    __table_args__ = (
        CheckConstraint("available_copies >= 0", name="chk_available_positive"),
        CheckConstraint("available_copies <= total_copies", name="chk_available_le_total"),
    )

    id = db.Column(db.Integer, primary_key=True)
    biblioteca_id = db.Column(db.Integer, db.ForeignKey("bibliotecas.id"), nullable=True)
    tipo_material = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    total_copies = db.Column(db.Integer, nullable=False, default=1)
    available_copies = db.Column(db.Integer, nullable=False, default=1)
    issue_number = db.Column(db.String(30))
    university = db.Column(db.String(150))
    loans = db.relationship("Prestamo", back_populates="material")
    __mapper_args__ = {"polymorphic_on": tipo_material, "polymorphic_identity": "material"}

    def __init__(
        self,
        title: str,
        isbn: str,
        total_copies: int = 1,
        available_copies: int = 1,
        issue_number: str | None = None,
        university: str | None = None,
        biblioteca_id: int | None = None,
    ) -> None:
        self.title = title
        self.isbn = isbn
        self.total_copies = total_copies
        self.available_copies = available_copies
        self.issue_number = issue_number
        self.university = university
        self.biblioteca_id = biblioteca_id

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.id}: {self.title!r}>"


class Libro(Material):
    __mapper_args__ = {"polymorphic_identity": "libro"}


class Revista(Material):
    __mapper_args__ = {"polymorphic_identity": "revista"}


class Tesis(Material):
    __mapper_args__ = {"polymorphic_identity": "tesis"}
