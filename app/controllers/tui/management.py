from app.model import catalogo
from app.view.management import management_rows
from collections.abc import Iterable

from textual.screen import Screen
from textual.widgets import Button, DataTable, Label
from textual.containers import Horizontal

from app.controllers.materiales import delete_material
from app.controllers.personas import delete_member
from app.controllers.prestamos import delete_loan, return_book
from app.controllers.usuarios import delete_user
from app.controllers.tui.forms import FormScreen


class ManagementScreen(Screen[None]):
    TITLES = {
        "users": "GESTION DE USUARIOS",
        "readers": "GESTION DE LECTORES",
        "materials": "GESTION DE MATERIALES",
        "loans": "GESTION DE PRESTAMOS",
    }

    def __init__(self, kind: str) -> None:
        super().__init__()
        self.kind = kind
        self.selected_id: int | None = None

    def compose(self):
        yield Label(self.TITLES[self.kind], classes="title")
        yield DataTable(cursor_type="row", id="records")
        yield Horizontal(
            Button("+ Nuevo", id="create", variant="success"),
            Button("Editar", id="update"),
            Button("Eliminar", id="delete", classes="danger"),
            Button("Devolver", id="return", variant="warning"),
            Button("Actualizar", id="refresh", classes="secondary"),
            Button("Volver", id="back", classes="secondary"),
            classes="toolbar",
        )
        yield Label("Selecciona una fila y usa botones o teclado.", id="message", classes="message")

    def on_mount(self) -> None:
        self.query_one("#return", Button).display = self.kind == "loans"
        self.refresh_table()

    def on_screen_resume(self):
        self.refresh_table()

    def refresh_table(self) -> None:
        table = self.query_one("#records", DataTable)
        table.clear(columns=True)
        rows = self.rows_for_kind()
        self.add_rows(table, rows[0], rows[1])

    def rows_for_kind(self):
        loaders = {
            "users": lambda: catalogo.people(staff=True),
            "readers": lambda: catalogo.people(readers=True),
            "materials": catalogo.materials,
            "loans": catalogo.loans,
        }
        return management_rows(self.kind, loaders[self.kind]())

    @staticmethod
    def add_rows(table: DataTable, columns: list[str], rows: Iterable[Iterable[object]]) -> None:
        table.add_columns(*columns)
        for row in rows:
            values = list(row)
            table.add_row(*(str(value) for value in values), key=str(values[0]))

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        self.selected_id = int(event.row_key.value)
        self.query_one("#message", Label).update(f"Registro seleccionado: {self.selected_id}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        action = event.button.id
        if action == "back":
            self.app.pop_screen()
        elif action == "refresh":
            self.refresh_table()
        elif action == "create":
            self.app.push_screen(FormScreen(self.kind))
        elif action == "update":
            self.edit_selected()
        elif action in {"delete", "return"}:
            self.mutate_selected(action)

    def edit_selected(self) -> None:
        if self.kind == "loans":
            self.notify("Los prestamos no se editan; usa devolver.", severity="warning")
        elif self.selected_id is None:
            self.notify("Selecciona un registro primero", severity="warning")
        else:
            self.app.push_screen(FormScreen(self.kind, self.selected_id))

    def mutate_selected(self, action: str) -> None:
        if self.selected_id is None:
            self.notify("Selecciona un registro primero", severity="warning")
            return
        try:
            if action == "return" and self.kind == "loans":
                return_book(self.selected_id)
            elif self.kind == "users":
                delete_user(self.selected_id)
            elif self.kind == "readers":
                delete_member(self.selected_id)
            elif self.kind == "materials":
                delete_material(self.selected_id)
            else:
                delete_loan(self.selected_id)
            self.selected_id = None
            self.refresh_table()
            self.notify("Operacion completada", severity="information")
        except Exception as error:
            self.notify(str(error), severity="error")
