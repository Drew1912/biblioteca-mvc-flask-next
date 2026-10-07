from secrets import token_hex
from werkzeug.security import check_password_hash, generate_password_hash
from app.main import db
from app.model.transaction import transactional
from app.model.validation import text, email_address, password_value


class Persona(db.Model):
    __tablename__ = "persona"

    id = db.Column(db.Integer, primary_key=True)
    biblioteca_id = db.Column(db.Integer, db.ForeignKey("bibliotecas.id"), nullable=True)
    tipo_persona = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    carnet_identidad = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    password_hash = db.Column(db.String(255), nullable=True)
    loans = db.relationship("Prestamo", back_populates="persona")
    __mapper_args__ = {"polymorphic_on": tipo_persona, "polymorphic_identity": "persona"}

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return bool(self.password_hash and check_password_hash(self.password_hash, password))

    @classmethod
    @transactional
    def create(cls, name, email, role, password=None, documento_identidad=None):
        user_type = ROLE_TYPES.get(text(role, "Rol").lower())
        if user_type is None:
            raise ValueError("Rol inválido")
        identity = text(documento_identidad, "Documento de identidad", 20) if documento_identidad else f"AUTO-{token_hex(6)}"
        user = user_type(name=text(name, "Nombre"), email=email_address(email), carnet_identidad=identity)
        if password:
            user.set_password(password_value(password))
        db.session.add(user)
        return user

    @classmethod
    def get(cls, user_id):
        user = db.session.get(cls, user_id)
        if user is None:
            raise ValueError("Usuario no encontrado")
        return user

    @transactional
    def update(self, name=None, email=None, documento_identidad=None):
        if name is not None:
            self.name = text(name, "Nombre")
        if email is not None:
            self.email = email_address(email)
        if documento_identidad is not None:
            self.carnet_identidad = text(documento_identidad, "Documento de identidad", 20)
        return self

    @transactional
    def delete(self):
        if self.loans:
            raise ValueError("No se puede eliminar un usuario con historial de préstamos")
        db.session.delete(self)

    @transactional
    def change_password(self, password):
        self.set_password(password_value(password))

    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter_by(email=email.strip().lower(), active=True).first()
        return user if user and user.check_password(password) else None

    @classmethod
    def active_user(cls, user_id):
        user = db.session.get(cls, user_id) if user_id else None
        return user if user and user.active else None

    @classmethod
    def get_reader(cls, member_id):
        member = cls.get(member_id)
        if member.tipo_persona not in {"estudiante", "docente"}:
            raise ValueError("Lector no encontrado")
        return member

    @classmethod
    def create_reader(cls, name, email, documento_identidad=None, role="estudiante", password=None):
        if role not in {"estudiante", "docente"}:
            raise ValueError("Rol de lector inválido")
        return cls.create(name, email, role, password, documento_identidad)


class Administrador(Persona):
    __mapper_args__ = {"polymorphic_identity": "administrador"}


class Bibliotecario(Persona):
    __mapper_args__ = {"polymorphic_identity": "bibliotecario"}


class Docente(Persona):
    __mapper_args__ = {"polymorphic_identity": "docente"}


class Estudiante(Persona):
    __mapper_args__ = {"polymorphic_identity": "estudiante"}


ROLE_TYPES = {
    "administrador": Administrador,
    "bibliotecario": Bibliotecario,
    "docente": Docente,
    "estudiante": Estudiante,
}
