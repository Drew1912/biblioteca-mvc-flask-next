import click
from sqlalchemy.exc import IntegrityError

from app.main import db
from app.model.catalogo import people
from app.model.usuarios import create_user, delete_user, get_user, update_user, set_user_password
from app.view.consola import print_rows


def register_user_commands(library: click.Group) -> None:
    @library.group("users")
    def users() -> None:
        """CRUD de usuarios por rol."""

    @users.command("create")
    @click.option("--name", required=True)
    @click.option("--email", required=True)
    @click.option("--role", type=click.Choice(["administrador", "bibliotecario", "doctor", "estudiante"]), required=True)
    def create_user_command(name: str, email: str, role: str) -> None:
        try:
            user = create_user(name, email, role)
        except (IntegrityError, ValueError) as error:
            db.session.rollback()
            raise click.ClickException(str(error))
        click.echo(f"Usuario creado: {user.id}")

    @users.command("list")
    def list_users() -> None:
        print_rows(["ID", "Nombre", "Email", "Rol", "Activo"],
                   ((user.id, user.name, user.email, user.tipo_persona, user.active)
                    for user in people()))

    @users.command("get")
    @click.option("--id", "user_id", type=int, required=True)
    def get_user_command(user_id: int) -> None:
        try:
            user = get_user(user_id)
        except ValueError as error:
            raise click.ClickException(str(error))
        print_rows(["ID", "Nombre", "Email", "Rol", "Activo"],
                   [[user.id, user.name, user.email, user.tipo_persona, user.active]])

    @users.command("update")
    @click.option("--id", "user_id", type=int, required=True)
    @click.option("--name")
    @click.option("--email")
    def update_user_command(user_id: int, name: str | None, email: str | None) -> None:
        try:
            update_user(user_id, name, email)
        except (IntegrityError, ValueError) as error:
            db.session.rollback()
            raise click.ClickException(str(error))
        click.echo("Usuario actualizado.")

    @users.command("delete")
    @click.option("--id", "user_id", type=int, required=True)
    def delete_user_command(user_id: int) -> None:
        try:
            delete_user(user_id)
        except ValueError as error:
            raise click.ClickException(str(error))
        click.echo("Usuario eliminado.")

    @users.command("password")
    @click.option("--id", "user_id", type=int, required=True)
    @click.password_option(confirmation_prompt=True)
    def password_command(user_id: int, password: str) -> None:
        """Asigna acceso web sin exigir login a la consola."""
        try:
            set_user_password(user_id, password)
        except ValueError as error:
            raise click.ClickException(str(error))
        click.echo("Contraseña actualizada.")
