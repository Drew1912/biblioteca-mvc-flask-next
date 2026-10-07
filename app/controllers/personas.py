from app.model.persona import Persona


def get_member(member_id):
    return Persona.get_reader(member_id)


def create_member(name, email, documento_identidad=None, role="estudiante", password=None):
    return Persona.create_reader(name, email, documento_identidad, role, password)


def update_member(member_id, name, email, documento_identidad=None):
    member = get_member(member_id)
    return member.update(name, email, documento_identidad)


def delete_member(member_id):
    member = get_member(member_id)
    member.delete()
