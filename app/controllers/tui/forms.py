from app.model.catalogo import materials as available_materials, people as active_people
from textual.containers import Center, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Input, Label, Select

from app.main import db
from app.model.materiales import create_material, update_material
from app.model.personas import create_member, update_member
from app.model.prestamos import checkout_book
from app.model.usuarios import create_user, update_user


class FormScreen(Screen[None]):
    def __init__(self, kind: str, record_id: int | None = None) -> None:
        super().__init__()
        self.kind = kind
        self.record_id = record_id

    def compose(self):
        title = "Actualizar" if self.record_id else "Crear"
        fields = self.form_fields()
        yield Center(Vertical(
            Label(f"{title} - {self.kind.title()}", classes="title"),
            *fields,
            Horizontal(Button("Guardar", id="save", variant="success"), Button("Cancelar", id="cancel")),
            classes="form",
        ))

    def form_fields(self):
        if self.kind == "users":
            fields = [Input(placeholder="Nombre", id="name"), Input(placeholder="Email", id="email")]
            if self.record_id is None:
                fields.append(Select([(role.title(), role) for role in ("administrador", "bibliotecario", "doctor", "estudiante")], prompt="Rol", id="role"))
            return fields
        if self.kind == "readers":
            return [Input(placeholder="Nombre", id="name"), Input(placeholder="Email", id="email")]
        if self.kind == "materials":
            if self.record_id is not None:
                return [Input(placeholder="Titulo", id="title"), Input(placeholder="ISBN", id="isbn")]
            return [Select([(kind.title(), kind) for kind in ("libro", "revista", "tesis")], prompt="Tipo", id="type"),
                    Input(placeholder="Titulo", id="title"), Input(placeholder="ISBN", id="isbn"), Input(placeholder="Copias", id="copies", type="integer")]
        materials = [(f"{x.title} · {x.tipo_material} · {x.available_copies} disponibles", x.id)
                     for x in available_materials(available=True)]
        people = [(f"{x.name} · {x.email} · {x.tipo_persona}", x.id)
                  for x in active_people(active=True)]
        return [Select(materials, prompt="Selecciona material", id="material"),
                Select(people, prompt="Selecciona persona", id="person"),
                Input(value="14", id="days", type="integer", placeholder="Dias del prestamo")]

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.app.pop_screen()
            return
        try:
            self.save()
            self.app.pop_screen()
            self.notify("Guardado correctamente", severity="information")
        except Exception as error:
            db.session.rollback()
            self.notify(str(error), severity="error")

    def input_value(self, field_id: str) -> str:
        return self.query_one(f"#{field_id}", Input).value.strip()

    def select_value(self, field_id: str) -> int:
        value = self.query_one(f"#{field_id}", Select).value
        if value is Select.BLANK:
            raise ValueError("Selecciona una opción antes de guardar")
        return int(value)

    def save(self) -> None:
        if self.kind == "users":
            if self.record_id:
                update_user(self.record_id, self.input_value("name") or None, self.input_value("email") or None)
            else:
                role = self.query_one("#role", Select).value
                if role is Select.BLANK:
                    raise ValueError("Selecciona un rol")
                create_user(self.input_value("name"), self.input_value("email"), str(role))
        elif self.kind == "readers":
            operation = update_member if self.record_id else create_member
            if self.record_id:
                operation(self.record_id, self.input_value("name") or None, self.input_value("email") or None)
            else:
                operation(self.input_value("name"), self.input_value("email"))
        elif self.kind == "materials":
            if self.record_id:
                update_material(self.record_id, self.input_value("title") or None, self.input_value("isbn") or None)
            else:
                material_type = self.query_one("#type", Select).value
                if material_type is Select.BLANK:
                    raise ValueError("Selecciona un tipo de material")
                create_material(str(material_type), self.input_value("title"), self.input_value("isbn"), int(self.input_value("copies")))
        else:
            checkout_book(self.select_value("material"), self.select_value("person"), int(self.input_value("days")))
