PYTHON := venv/bin/python
FLASK := $(PYTHON) -m flask --app app.main:create_app
PODMAN_COMPOSE := podman-compose

.PHONY: install test lint init-db seed console run build up down logs clean

install:
	$(PYTHON) -m pip install -e '.[dev]'

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
	$(FLASK) seed --reset

console:
	$(FLASK) console

run:
	$(FLASK) library --help

build:
	$(PODMAN_COMPOSE) build

up:
	$(PODMAN_COMPOSE) up -d --force-recreate

down:
	$(PODMAN_COMPOSE) down

logs:
	$(PODMAN_COMPOSE) logs -f

clean:
	find . -type d -name '__pycache__' -prune -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf *.egg-info

web-build:
	pnpm --dir web build

web-test:
	pnpm --dir web test
