from app.controllers.tui import FormScreen, LibraryTui, ReportScreen


def run_console() -> None:
    LibraryTui().run()


__all__ = ["FormScreen", "LibraryTui", "ReportScreen", "run_console"]
