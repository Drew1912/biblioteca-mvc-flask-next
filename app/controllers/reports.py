import click

from app.model.reportes import summary
from app.view.consola import print_rows


def register_report_commands(library: click.Group) -> None:
    @library.command("reports")
    def reports() -> None:
        """Muestra el resumen de la biblioteca."""
        data = summary()
        print_rows(["Indicador", "Cantidad"],
                   [["Materiales", data["materiales"]],
                    ["Copias disponibles", data["copias_disponibles"]],
                    ["Usuarios", data["usuarios"]],
                    ["Préstamos activos", data["prestamos_activos"]],
                    ["Préstamos vencidos", data["prestamos_vencidos"]]])
