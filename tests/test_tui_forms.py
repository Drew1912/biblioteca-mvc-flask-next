import asyncio
from textual.widgets import Input, Select
from app.controllers.console import LibraryTui, FormScreen
from app.model.material import Material
from app.model.persona import Persona


def test_tui_creates_material_and_reader(app):
    async def exercise():
        async with LibraryTui().run_test(size=(120, 45)) as pilot:
            pilot.app.push_screen(FormScreen("materials"))
            await pilot.pause()
            screen = pilot.app.screen
            screen.query_one("#type", Select).value = "libro"
            screen.query_one("#title", Input).value = "Libro Textual"
            screen.query_one("#isbn", Input).value = "TUI"
            screen.query_one("#copies", Input).value = "2"
            await pilot.click("#save")
            await pilot.pause()
            assert Material.query.one().title == "Libro Textual"
            pilot.app.push_screen(FormScreen("readers"))
            await pilot.pause()
            screen = pilot.app.screen
            screen.query_one("#name", Input).value = "Lector Textual"
            screen.query_one("#email", Input).value = "tui@test.local"
            await pilot.click("#save")
            await pilot.pause()
            assert Persona.query.one().name == "Lector Textual"
    with app.app_context():
        asyncio.run(exercise())
