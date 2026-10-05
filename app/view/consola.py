from collections.abc import Iterable


def print_rows(headers: list[str], rows: Iterable[Iterable[object]]) -> None:
    values = [[str(value) for value in row] for row in rows]
    widths = [len(header) for header in headers]
    for row in values:
        widths = [max(width, len(value)) for width, value in zip(widths, row)]
    print(" | ".join(header.ljust(width) for header, width in zip(headers, widths)))
    print("-+-".join("-" * width for width in widths))
    for row in values:
        print(" | ".join(value.ljust(width) for value, width in zip(row, widths)))