from app.model import db


class Biblioteca:
    """Agregado de dominio que representa el catálogo de la biblioteca."""
    __tablename__ = 'bibliotecas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    
    # Relaciones (Permiten acceder a las personas y materiales desde la biblioteca)
    personas = db.relationship('Persona', backref='biblioteca', lazy=True)
    
    # Esta relación requiere que el archivo material.py ya esté configurado con ORM
    # materiales = db.relationship('Material', backref='biblioteca', lazy=True)
    # def __init__(self, nombre: str):
    #     self.nombre = nombre
