import asyncio

from app import create_app
from app.controllers.console import LibraryTui
from app.controllers.console import FormScreen, ReportScreen
from main import db
from app.model.materiales import create_material
from app.model.personas import create_member
from textual.widgets import Select


def test_tui_opens_reports_from_main_menu():
    flask_app = create_app(
        {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"}
    )

    async def exercise_tui():
        with flask_app.app_context():
            db.create_all()
            async with LibraryTui().run_test() as pilot:
                for _ in range(4):
                    await pilot.press("tab")
                await pilot.press("enter")
                await pilot.pause()
                assert pilot.app.screen_stack[-1].__class__.__name__ == "ReportScreen"
                await pilot.press("escape")
                await pilot.pause()
                assert pilot.app.screen_stack[-1].__class__.__name__ == "Screen"

    asyncio.run(exercise_tui())


def test_tui_uses_named_selectors_for_loans_and_reports(app):
    with app.app_context():
        material = create_material("tesis", "Tesis de prueba", "TEST-TESIS", 1)
        reader = create_member("Lector", "lector@test.local")

        async def exercise_tui():
            async with LibraryTui().run_test() as pilot:
                pilot.app.push_screen(FormScreen("loans"))
                await pilot.pause()
                material_options = pilot.app.screen.query_one("#material")._options
                reader_options = pilot.app.screen.query_one("#person")._options
                assert [value for _, value in material_options if value not in (None, Select.BLANK)] == [material.id]
                assert [value for _, value in reader_options if value not in (None, Select.BLANK)] == [reader.id]
                pilot.app.pop_screen()
                pilot.app.push_screen(ReportScreen())
                await pilot.pause()
                report_select = pilot.app.screen.query_one("#report-choice")
                report_select.value = "inventory"
                await pilot.pause()
                assert len(pilot.app.screen.query_one("#report-table").columns) == 5

        asyncio.run(exercise_tui())
