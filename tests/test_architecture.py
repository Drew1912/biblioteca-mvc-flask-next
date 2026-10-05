from pathlib import Path


def test_mvc_boundaries():
    folders = {p.name for p in Path("app").iterdir() if p.is_dir() and p.name != "__pycache__"}
    assert folders == {"model", "controllers", "view"}
    assert Path("app/main.py").is_file()
    assert not Path("app/extensions.py").exists()


def test_source_line_limit():
    sources = [*Path("app").rglob("*.py"), *Path("tests").glob("*.py")]
    for folder in ["app", "model", "controllers", "view", "tests"]:
        sources.extend(Path("web", folder).rglob("*.ts"))
        sources.extend(Path("web", folder).rglob("*.tsx"))
        sources.extend(Path("web", folder).rglob("*.css"))
    oversized = [f"{p}: {len(p.read_text().splitlines())}" for p in sources if len(p.read_text().splitlines()) > 130]
    assert not oversized, "Archivos que exceden 130 líneas: " + ", ".join(oversized)


def test_model_has_no_presentation_dependencies():
    for source in Path("app/model").glob("*.py"):
        text = source.read_text()
        assert "from app.controllers" not in text
        assert "from app.view" not in text
        assert "import textual" not in text
