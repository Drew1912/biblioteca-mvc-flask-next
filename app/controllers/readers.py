import click
from sqlalchemy.exc import IntegrityError

from main import db
from app.model.persona import Estudiante
from app.model.personas import create_member, delete_member, get_member, update_member
from app.view.consola import print_rows


def register_reader_commands(library: click.Group) -> None:
    @library.group("readers")
    def readers() -> None:
        """CRUD de lectores."""

    @readers.command("create")
    @click.option("--name", required=True)
    @click.option("--email", required=True)
    def create_reader(name: str, email: str) -> None:
        try:
            reader = create_member(name, email)
        except IntegrityError:
            db.session.rollback()
            raise click.ClickException("El email ya está registrado")
        click.echo(f"Lector creado: {reader.id}")

    @readers.command("list")
    def list_readers() -> None:
        print_rows(["ID", "Nombre", "Email", "Activo"],
                   ((reader.id, reader.name, reader.email, reader.active)
                    for reader in Estudiante.query.order_by(Estudiante.id).all()))

    @readers.command("get")
    @click.option("--id", "reader_id", type=int, required=True)
    def get_reader(reader_id: int) -> None:
        try:
            reader = get_member(reader_id)
        except ValueError as error:
            raise click.ClickException(str(error))
        print_rows(["ID", "Nombre", "Email", "Activo"],
                   [[reader.id, reader.name, reader.email, reader.active]])

    @readers.command("update")
    @click.option("--id", "reader_id", type=int, required=True)
    @click.option("--name")
    @click.option("--email")
    def update_reader(reader_id: int, name: str | None, email: str | None) -> None:
        try:
            update_member(reader_id, name, email)
        except (IntegrityError, ValueError) as error:
            db.session.rollback()
            raise click.ClickException(str(error))
        click.echo("Lector actualizado.")

    @readers.command("delete")
    @click.option("--id", "reader_id", type=int, required=True)
    def delete_reader(reader_id: int) -> None:
        try:
            delete_member(reader_id)
        except ValueError as error:
            raise click.ClickException(str(error))
        click.echo("Lector eliminado.")
