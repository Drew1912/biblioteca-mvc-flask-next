import click
from flask import Flask

from app.controllers.loans import register_loan_commands
from app.controllers.materials import register_material_commands
from app.controllers.readers import register_reader_commands
from app.controllers.reports import register_report_commands
from app.controllers.users import register_user_commands
from app.controllers.console import run_console
from app.model.schema import initialize_database
from app.model.seed import seed_database


def register_cli(app: Flask) -> None:
    @app.cli.command("console")
    def console() -> None:
        """Abre el TUI interactivo de la biblioteca."""
        initialize_database()
        run_console()

    @app.cli.command("init-db")
    def init_db() -> None:
        """Crea las tablas de la base de datos."""
        initialize_database()
        click.echo("Base de datos inicializada.")

    @app.cli.command("seed")
    @click.option("--reset", is_flag=True, help="Borra los datos actuales antes de sembrar.")
    def seed(reset: bool) -> None:
        """Carga datos de prueba: 20 materiales, 40 personas y 20 préstamos."""
        initialize_database()
        counts = seed_database(reset=reset)
        click.echo(
            f"Datos listos: {counts['materiales']} materiales, "
            f"{counts['personas']} personas y {counts['prestamos']} préstamos."
        )

    @app.cli.group("library")
    def library() -> None:
        """Administra la biblioteca desde comandos de consola."""

    register_user_commands(library)
    register_reader_commands(library)
    register_material_commands(library)
    register_loan_commands(library)
    register_report_commands(library)
