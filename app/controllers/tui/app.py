from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label

from app.controllers.tui.management import ManagementScreen
from app.controllers.tui.reports_screen import ReportScreen


class LibraryTui(App[None]):
    CSS = """
    Screen { background: $surface; }
    #main-menu { align: center middle; width: 60%; height: 80%; border: round $primary; padding: 2 4; }
    #main-menu Button { width: 100%; margin: 1 0; }
    .title { text-style: bold; color: $accent; width: 100%; content-align: center middle; margin: 1; }
    .toolbar { height: auto; align: center middle; padding: 1; }
    .toolbar Button { margin: 0 1; min-width: 14; }
    .secondary { background: $panel; }
    .danger { background: $error; }
    DataTable { height: 1fr; margin: 1 2; }
    .form { width: 70%; height: auto; border: round $primary; padding: 1 2; }
    .form Input, .form Select { width: 100%; margin: 1 0; }
    .message { height: 2; color: $success; padding: 1 2; }
    """
    BINDINGS = [("q", "quit", "Salir")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Container(
            Label("BIBLIOTECA", classes="title"),
            Button("Usuarios", id="users", variant="primary"),
            Button("Lectores", id="readers", variant="primary"),
            Button("Materiales", id="materials", variant="primary"),
            Button("Prestamos", id="loans", variant="primary"),
            Button("Reportes", id="reports", variant="success"),
            Button("Salir", id="exit", variant="error"),
            id="main-menu",
        )
        yield Footer()

    def action_quit(self) -> None:
        self.exit()

    @on(Button.Pressed, "#reports")
    def open_reports(self) -> None:
        self.push_screen(ReportScreen())

    @on(Button.Pressed, "#users, #readers, #materials, #loans")
    def open_management(self, event: Button.Pressed) -> None:
        self.push_screen(ManagementScreen(event.button.id or "materials"))

    @on(Button.Pressed, "#exit")
    def close_application(self) -> None:
        self.exit()
