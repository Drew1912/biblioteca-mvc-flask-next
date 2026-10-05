from app.model.material import Material
from app.model.persona import Persona
from app.model.prestamo import Prestamo


def materials(available=False):
    query = Material.query
    if available:
        query = query.filter(Material.available_copies > 0)
    return query.order_by(Material.title).all()


def people(active=False, readers=False):
    query = Persona.query
    if active:
        query = query.filter_by(active=True)
    if readers:
        query = query.filter_by(tipo_persona="estudiante")
    return query.order_by(Persona.name).all()


def loans(user=None):
    query = Prestamo.query
    if user and user.tipo_persona not in {"administrador", "bibliotecario"}:
        query = query.filter_by(persona_id=user.id)
    return query.order_by(Prestamo.due_at).all()


def management_rows(kind):
    if kind == "users":
        return (["ID", "Nombre", "Email", "Rol", "Activo"],
                [(x.id, x.name, x.email, x.tipo_persona, x.active) for x in people()])
    if kind == "readers":
        return (["ID", "Nombre", "Email", "Activo"],
                [(x.id, x.name, x.email, x.active) for x in people(readers=True)])
    if kind == "materials":
        return (["ID", "Tipo", "Título", "ISBN", "Disponibles"],
                [(x.id, x.tipo_material, x.title, x.isbn, f"{x.available_copies}/{x.total_copies}")
                 for x in materials()])
    return (["ID", "Material", "Persona", "Vence", "Devuelto"],
            [(x.id, x.material.title, x.persona.name, x.due_at.strftime("%Y-%m-%d"),
              "Si" if x.returned_at else "No") for x in loans()])
