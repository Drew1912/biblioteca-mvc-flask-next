from app.model.biblioteca import Biblioteca
from app.model.material import Libro, Material, Revista, Tesis
from app.model.persona import Administrador, Bibliotecario, Doctor, Estudiante, Persona
from app.model.prestamo import Prestamo

__all__ = [
    "Administrador", "Biblioteca", "Bibliotecario", "Doctor", "Estudiante",
    "Libro", "Material", "Persona", "Prestamo", "Revista", "Tesis",
]