from app.main import db


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


class Libro(Material):
    __mapper_args__ = {"polymorphic_identity": "libro"}


class Revista(Material):
    __mapper_args__ = {"polymorphic_identity": "revista"}


class Tesis(Material):
    __mapper_args__ = {"polymorphic_identity": "tesis"}
