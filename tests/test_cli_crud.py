import pytest


@pytest.mark.parametrize("group,create_args,update_args", [
    ("materials", ["--type", "revista", "--title", "Inicial", "--isbn", "CLI"], ["--title", "Editado"]),
    ("users", ["--name", "Inicial", "--email", "u@test.local", "--role", "docente"], ["--name", "Editado"]),
    ("readers", ["--name", "Inicial", "--email", "r@test.local"], ["--name", "Editado"]),
])
def test_cli_crud(runner, group, create_args, update_args):
    def invoke(*args):
        result = runner.invoke(args=["library", group, *args])
        assert result.exit_code == 0, result.output
        return result.output
    invoke("create", *create_args)
    assert "Inicial" in invoke("list")
    invoke("update", "--id", "1", *update_args)
    assert "Editado" in invoke("get", "--id", "1")
    invoke("delete", "--id", "1")
    assert "Editado" not in invoke("list")
    assert runner.invoke(args=["library", group, "get", "--id", "999"]).exit_code != 0


def test_password_command(app, runner, account):
    from app.controllers.usuarios import authenticate
    user_id = account()
    result = runner.invoke(args=["library", "users", "password", "--id", str(user_id)],
                           input="NuevaClave123!\nNuevaClave123!\n")
    assert result.exit_code == 0
    assert "NuevaClave123!" not in result.output
    with app.app_context():
        assert authenticate("administrador@test.local", "NuevaClave123!")
        assert authenticate("administrador@test.local", "Biblioteca123!") is None


def test_cli_loan_lifecycle(app, runner, account):
    from app.controllers.materiales import create_book
    person_id = account("estudiante")
    with app.app_context():
        book_id = create_book("CLI préstamo", "CLI-L", 1).id
    commands = [["create", "--material-id", str(book_id), "--reader-id", str(person_id)],
                ["list"], ["get", "--id", "1"], ["return", "--id", "1"], ["delete", "--id", "1"]]
    for args in commands:
        result = runner.invoke(args=["library", "loans", *args])
        assert result.exit_code == 0, result.output


def test_cli_teacher_reader_and_report(runner):
    created = runner.invoke(args=["library", "readers", "create", "--name", "Profesora",
                                  "--email", "prof@test.local", "--role", "docente"])
    assert created.exit_code == 0
    report = runner.invoke(args=["library", "reports", "--type", "readers"])
    assert report.exit_code == 0
    assert "docente" in report.output
    assert "Profesora" in report.output
