from app.main import db
from werkzeug.security import check_password_hash, generate_password_hash


class Persona(db.Model):
    __tablename__ = "persona"

    id = db.Column(db.Integer, primary_key=True)
    
    # Llave foránea conectando con Biblioteca según el diagrama UML
    biblioteca_id = db.Column(db.Integer, db.ForeignKey('bibliotecas.id'), nullable=True)
    tipo_persona = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    
    # Nuevo: Identificador oficial necesario para préstamos físicos
    cod_estudiante = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    password_hash = db.Column(db.String(255), nullable=True)
    
    
    loans = db.relationship("Prestamo", back_populates="persona")
    __mapper_args__ = {"polymorphic_on": tipo_persona, "polymorphic_identity": "persona"}

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return bool(self.password_hash and check_password_hash(self.password_hash, password))


class Administrador(Persona):
    __mapper_args__ = {"polymorphic_identity": "administrador"}


class Bibliotecario(Persona):
    __mapper_args__ = {"polymorphic_identity": "bibliotecario"}


class Docente(Persona):
    __mapper_args__ = {"polymorphic_identity": "docente"}


class Estudiante(Persona):
    __mapper_args__ = {"polymorphic_identity": "estudiante"}
