import click

from app.model import reportes
from app.view.consola import print_rows


REPORTS = {
    "inventory": (["Tipo", "Título", "ISBN", "Copias", "Disponibles"], reportes.inventory_rows),
    "users": (["Rol", "Nombre", "Correo", "Estado"], reportes.users_by_role_rows),
    "readers": (["Rol", "Nombre", "Correo", "Estado"], reportes.readers_rows),
    "loans": (["Material", "Persona", "Vence", "Estado"], reportes.loans_rows),
    "overdue": (["Material", "Persona", "Vence", "Días de retraso"], reportes.overdue_rows),
}


def register_report_commands(library: click.Group) -> None:
    @library.command("reports")
    @click.option("--type", "report_type", type=click.Choice(["summary", *REPORTS]), default="summary")
    def reports(report_type: str) -> None:
        """Muestra resumen, usuarios, lectores, inventario o préstamos."""
        if report_type != "summary":
            columns, rows = REPORTS[report_type]
            print_rows(columns, rows())
            return
        data = reportes.summary()
        print_rows(["Indicador", "Cantidad"],
                   [["Materiales", data["materiales"]],
                    ["Copias disponibles", data["copias_disponibles"]],
                    ["Usuarios", data["usuarios"]],
                    ["Préstamos activos", data["prestamos_activos"]],
                    ["Préstamos vencidos", data["prestamos_vencidos"]]])
