from app.model.material import Material
from app.model.persona import Persona
from app.model.prestamo import Prestamo


def materials(available=False):
    query = Material.query
    if available:
        query = query.filter(Material.available_copies > 0)
    return query.order_by(Material.title).all()


def people(active=False, readers=False, staff=False):
    query = Persona.query
    if active:
        query = query.filter_by(active=True)
    if readers:
        query = query.filter(Persona.tipo_persona.in_(("estudiante", "docente")))
    if staff:
        query = query.filter(Persona.tipo_persona.in_(("administrador", "bibliotecario")))
    return query.order_by(Persona.name).all()


def loans(user=None):
    query = Prestamo.query
    if user and user.tipo_persona not in {"administrador", "bibliotecario"}:
        query = query.filter_by(persona_id=user.id)
    return query.order_by(Prestamo.due_at).all()
