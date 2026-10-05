from app.model.usuarios import create_user, delete_user, get_user, update_user


def get_member(member_id):
    member = get_user(member_id)
    if member.tipo_persona != "estudiante":
        raise ValueError("Lector no encontrado")
    return member


def create_member(name, email):
    return create_user(name, email, "estudiante")


def update_member(member_id, name, email):
    get_member(member_id)
    return update_user(member_id, name, email)


def delete_member(member_id):
    get_member(member_id)
    delete_user(member_id)
