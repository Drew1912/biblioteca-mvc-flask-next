"""Genera DIAGRAMAS.md desde la plantilla documental."""

from pathlib import Path


def main() -> None:
    folder = Path(__file__).parent
    source = folder / "DIAGRAMAS_PLANTILLA.md"
    target = folder / "DIAGRAMAS.md"
    target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Documento generado: {target}")


if __name__ == "__main__":
    main()
