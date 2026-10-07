from app.main import db


class Biblioteca(db.Model):
    """Agregado de dominio que representa el catálogo de la biblioteca."""
    __tablename__ = 'bibliotecas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    
    personas = db.relationship('Persona', backref='biblioteca', lazy=True)
