from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.model.biblioteca import Biblioteca
from app.model.material import Libro, Material, Revista, Tesis
from app.model.persona import Administrador, Bibliotecario, Docente, Estudiante, Persona
from app.model.prestamo import Prestamo

__all__ = [
    "Administrador", "Biblioteca", "Bibliotecario", "Docente", "Estudiante",
    "Libro", "Material", "Persona", "Prestamo", "Revista", "Tesis",
]
