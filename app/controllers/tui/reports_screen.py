from textual import on
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Button, DataTable, Label, Select

from app.model.reportes import inventory_rows, loans_rows, overdue_rows, summary, users_by_role_rows, readers_rows


class ReportScreen(Screen[None]):
    BINDINGS = [("escape", "back", "Volver")]

    def compose(self):
        yield Label("REPORTES", classes="title")
        yield Select([
            ("Resumen general", "summary"),
            ("Inventario por tipo", "inventory"),
            ("Usuarios internos", "users"),
            ("Lectores por rol", "readers"),
            ("Historial de préstamos", "loans"),
            ("Préstamos vencidos", "overdue"),
        ], value="summary", id="report-choice")
        yield DataTable(id="report-table")
        yield Horizontal(Button("Actualizar", id="refresh", variant="primary"), Button("Volver", id="back", classes="secondary"), classes="toolbar")

    def on_mount(self) -> None:
        self.refresh_report("summary")

    @on(Select.Changed, "#report-choice")
    def select_report(self, event: Select.Changed) -> None:
        if event.value is not Select.BLANK:
            self.refresh_report(str(event.value))

    def refresh_report(self, report_type: str) -> None:
        table = self.query_one("#report-table", DataTable)
        table.clear(columns=True)
        columns, rows = self.report_data(report_type)
        table.add_columns(*columns)
        for row in rows:
            table.add_row(*(str(value) for value in row))

    @staticmethod
    def report_data(report_type: str):
        if report_type == "inventory":
            return (["Tipo", "Material", "ISBN", "Total", "Disponibles"], inventory_rows())
        if report_type == "users":
            return (["Rol", "Nombre", "Email", "Estado"], users_by_role_rows())
        if report_type == "readers":
            return (["Rol", "Nombre", "Email", "Estado"], readers_rows())
        if report_type == "loans":
            return (["Material", "Persona", "Vence", "Estado"], loans_rows())
        if report_type == "overdue":
            return (["Material", "Persona", "Vence", "Días vencido"], overdue_rows())
        data = summary()
        return (["Indicador", "Cantidad"], [
            ("Materiales registrados", data["materiales"]),
            ("Copias disponibles", data["copias_disponibles"]),
            ("Usuarios registrados", data["usuarios"]),
            ("Préstamos activos", data["prestamos_activos"]),
            ("Préstamos vencidos", data["prestamos_vencidos"]),
        ])

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()
        else:
            self.refresh_report(str(self.query_one("#report-choice", Select).value))

    def action_back(self) -> None:
        self.app.pop_screen()
