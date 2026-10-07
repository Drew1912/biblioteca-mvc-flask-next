def management_rows(kind, records):
    if kind == "users":
        return (["ID", "Nombre", "Email", "Rol", "Activo"],
                [(x.id, x.name, x.email, x.tipo_persona, x.active) for x in records])
    if kind == "readers":
        return (["ID", "Nombre", "Email", "Activo"],
                [(x.id, x.name, x.email, x.active) for x in records])
    if kind == "materials":
        return (["ID", "Tipo", "Título", "ISBN", "Disponibles"],
                [(x.id, x.tipo_material, x.title, x.isbn, f"{x.available_copies}/{x.total_copies}")
                 for x in records])
    return (["ID", "Material", "Persona", "Vence", "Devuelto"],
            [(x.id, x.material.title, x.persona.name, x.due_at.strftime("%Y-%m-%d"),
              "Si" if x.returned_at else "No") for x in records])
