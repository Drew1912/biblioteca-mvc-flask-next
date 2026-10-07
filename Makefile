ifeq ($(OS),Windows_NT)
PYTHON ?= $(if $(wildcard venv/Scripts/python.exe),venv/Scripts/python.exe,python)
else
PYTHON ?= $(if $(wildcard venv/bin/python),venv/bin/python,python3)
endif
FLASK := $(PYTHON) -m flask --app app.main:create_app
COMPOSE ?= docker compose

.PHONY: install test lint init-db seed console run build up down logs clean web-build web-test

install:
	$(PYTHON) -m pip install -e ".[dev]"

test:
	$(PYTHON) -m pytest -q

lint:
	$(PYTHON) -m compileall -q app tests
	$(PYTHON) -m ruff check app tests
	$(PYTHON) -m pytest -q tests/test_architecture.py
	pnpm --dir web lint

init-db:
	$(FLASK) init-db

seed:
	$(FLASK) seed

console:
	$(FLASK) console

run:
	$(FLASK) library --help

build:
	$(COMPOSE) build

up:
	$(COMPOSE) up -d --force-recreate

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f

clean:
	$(PYTHON) -c "import pathlib, shutil; [shutil.rmtree(path) for path in pathlib.Path('.').rglob('__pycache__')]; shutil.rmtree('.pytest_cache', ignore_errors=True); [shutil.rmtree(path) for path in pathlib.Path('.').glob('*.egg-info') if path.is_dir()]"

web-build:
	pnpm --dir web build

web-test:
	pnpm --dir web test
