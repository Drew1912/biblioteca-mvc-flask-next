PYTHON := venv/bin/python
FLASK := $(PYTHON) -m flask --app main:create_app
PODMAN_COMPOSE := podman-compose

.PHONY: install test lint init-db seed console run build up down logs clean

install:
	$(PYTHON) -m pip install -e '.[dev]'

test:
	$(PYTHON) -m pytest -q

lint:
	$(PYTHON) -m compileall -q app tests

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
	$(PODMAN_COMPOSE) up -d

down:
	$(PODMAN_COMPOSE) down

logs:
	$(PODMAN_COMPOSE) logs -f

clean:
	find . -type d -name '__pycache__' -prune -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf *.egg-info