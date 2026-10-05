import click

from app.model.catalogo import loans as list_loans_data
from app.model.prestamos import checkout_book, delete_loan, get_loan, return_book
from app.view.consola import print_rows


def register_loan_commands(library: click.Group) -> None:
    @library.group("loans")
    def loans() -> None:
        """CRUD y operaciones de préstamos."""

    @loans.command("create")
    @click.option("--material-id", type=int, required=True)
    @click.option("--reader-id", type=int, required=True)
    @click.option("--days", type=click.IntRange(min=1), default=14)
    def create_loan(material_id: int, reader_id: int, days: int) -> None:
        try:
            loan = checkout_book(material_id, reader_id, days)
        except ValueError as error:
            raise click.ClickException(str(error))
        click.echo(f"Préstamo creado: {loan.id}")

    @loans.command("list")
    def list_loans() -> None:
        print_rows(["ID", "Material", "Persona", "Vence", "Devuelto"],
                   ((loan.id, loan.material.title, loan.persona.name, loan.due_at.isoformat(), loan.returned_at or "No")
                    for loan in list_loans_data()))

    @loans.command("get")
    @click.option("--id", "loan_id", type=int, required=True)
    def get_loan_command(loan_id: int) -> None:
        try:
            loan = get_loan(loan_id)
        except ValueError as error:
            raise click.ClickException(str(error))
        print_rows(["ID", "Material", "Persona", "Vence", "Devuelto"],
                   [[loan.id, loan.material.title, loan.persona.name, loan.due_at, loan.returned_at or "No"]])

    @loans.command("return")
    @click.option("--id", "loan_id", type=int, required=True)
    def return_loan(loan_id: int) -> None:
        try:
            return_book(loan_id)
        except ValueError as error:
            raise click.ClickException(str(error))
        click.echo("Devolución registrada.")

    @loans.command("delete")
    @click.option("--id", "loan_id", type=int, required=True)
    def delete_loan_command(loan_id: int) -> None:
        try:
            delete_loan(loan_id)
        except ValueError as error:
            raise click.ClickException(str(error))
        click.echo("Préstamo eliminado.")
