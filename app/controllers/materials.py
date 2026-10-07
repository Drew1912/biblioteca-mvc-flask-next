import click
from sqlalchemy.exc import IntegrityError

from app.model.catalogo import materials as list_materials_data
from app.controllers.materiales import create_material, delete_material, get_material, update_material
from app.view.consola import print_rows


def register_material_commands(library: click.Group) -> None:
    @library.group("materials")
    def materials() -> None:
        """CRUD de materiales."""

    @materials.command("create")
    @click.option("--type", "material_type", type=click.Choice(["libro", "revista", "tesis"]), required=True)
    @click.option("--title", required=True)
    @click.option("--isbn", required=True)
    @click.option("--copies", type=click.IntRange(min=1), default=1)
    def create_material_command(material_type: str, title: str, isbn: str, copies: int) -> None:
        try:
            material = create_material(material_type, title, isbn, copies)
        except (IntegrityError, ValueError) as error:
            raise click.ClickException(str(error))
        click.echo(f"Material creado: {material.id}")

    @materials.command("list")
    def list_materials() -> None:
        print_rows(["ID", "Tipo", "Título", "ISBN", "Disponibles"],
                   ((item.id, item.tipo_material, item.title, item.isbn, f"{item.available_copies}/{item.total_copies}")
                    for item in list_materials_data()))

    @materials.command("get")
    @click.option("--id", "material_id", type=int, required=True)
    def get_material_command(material_id: int) -> None:
        try:
            item = get_material(material_id)
        except ValueError as error:
            raise click.ClickException(str(error))
        print_rows(["ID", "Tipo", "Título", "ISBN", "Disponibles"],
                   [[item.id, item.tipo_material, item.title, item.isbn, f"{item.available_copies}/{item.total_copies}"]])

    @materials.command("update")
    @click.option("--id", "material_id", type=int, required=True)
    @click.option("--title")
    @click.option("--isbn")
    def update_material_command(material_id: int, title: str | None, isbn: str | None) -> None:
        try:
            update_material(material_id, title, isbn)
        except (IntegrityError, ValueError) as error:
            raise click.ClickException(str(error))
        click.echo("Material actualizado.")

    @materials.command("delete")
    @click.option("--id", "material_id", type=int, required=True)
    def delete_material_command(material_id: int) -> None:
        try:
            delete_material(material_id)
        except ValueError as error:
            raise click.ClickException(str(error))
        click.echo("Material eliminado.")
