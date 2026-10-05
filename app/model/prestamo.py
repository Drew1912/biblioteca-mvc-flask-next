from datetime import UTC, datetime

from app.main import db


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

    @property
    def book(self):
        return self.material

    @property
    def member(self):
        return self.persona
