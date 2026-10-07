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


def test_database_instance_lives_only_in_orchestrator():
    sources = [p for p in Path("app").rglob("*.py") if "SQLAlchemy()" in p.read_text()]
    assert sources == [Path("app/main.py")]


def test_frontend_entries_and_views_do_not_call_transport():
    for folder in ("app", "view"):
        for source in Path("web", folder).rglob("*.tsx"):
            assert "fetch(" not in source.read_text()
            assert "await api(" not in source.read_text()


def test_management_controllers_have_no_database_operations():
    for source in Path("app/controllers").rglob("*.py"):
        content = source.read_text()
        assert "from app.main import db" not in content, source
        assert "db.session" not in content, source
        assert ".query.filter" not in content, source
    for name in ("materiales", "usuarios", "personas", "prestamos"):
        assert Path("app/controllers", f"{name}.py").is_file()
        assert not Path("app/model", f"{name}.py").exists()


def test_python_views_have_no_database_operations():
    for source in Path("app/view").rglob("*.py"):
        content = source.read_text()
        assert "db.session" not in content, source
        assert ".query" not in content, source
