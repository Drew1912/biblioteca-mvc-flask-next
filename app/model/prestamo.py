from datetime import UTC, datetime, timedelta

from app.main import db
from app.model.material import Material
from app.model.persona import Persona
from app.model.transaction import transactional


class Prestamo(db.Model):
    __tablename__ = "prestamo"

    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey("material.id"), nullable=False)
    persona_id = db.Column(db.Integer, db.ForeignKey("persona.id"), nullable=False)
    loaned_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))
    due_at = db.Column(db.DateTime, nullable=False)
    returned_at = db.Column(db.DateTime)
    material = db.relationship("Material", back_populates="loans")
    persona = db.relationship("Persona", back_populates="loans")

    @classmethod
    @transactional
    def checkout(cls, book_id: int, member_id: int, days: int):
        book = Material.query.filter_by(id=book_id).with_for_update().first()
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
        loan = cls(material=book, persona=member, due_at=datetime.now(UTC) + timedelta(days=days))
        db.session.add(loan)
        return loan

    @classmethod
    def get(cls, loan_id: int):
        loan = db.session.get(cls, loan_id)
        if loan is None:
            raise ValueError("Préstamo no encontrado")
        return loan

    @classmethod
    @transactional
    def return_material(cls, loan_id: int):
        loan = cls.query.filter_by(id=loan_id).with_for_update().first()
        if loan is None:
            raise ValueError("Préstamo no encontrado")
        db.session.refresh(loan.material, with_for_update=True)
        if loan.returned_at is not None:
            raise ValueError("El préstamo ya fue devuelto")
        loan.returned_at = datetime.now(UTC)
        loan.material.available_copies += 1
        return loan

    @transactional
    def delete(self):
        if self.returned_at is None:
            self.material.available_copies += 1
        db.session.delete(self)

    @property
    def book(self):
        return self.material

    @property
    def member(self):
        return self.persona
