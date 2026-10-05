# Desarrollo

## Preparación

```bash
python3 -m venv venv
source venv/bin/activate
make install
```

## Ejecución

```bash
make init-db
make seed
make console
```

`make console` abre el TUI. El usuario puede navegar con mouse, Tab, flechas, Enter y Escape.

## Comandos CLI

```bash
venv/bin/python -m flask --app app:create_app library users list
venv/bin/python -m flask --app app:create_app library readers list
venv/bin/python -m flask --app app:create_app library materials list
venv/bin/python -m flask --app app:create_app library loans list
venv/bin/python -m flask --app app:create_app library reports
venv/bin/python -m flask --app app:create_app seed --reset
```

## Podman

```bash
podman-compose config
make build
make up
podman-compose run --rm app flask --app app:create_app seed --reset
```

La imagen de PostgreSQL usa una referencia completa de registro para funcionar en hosts Podman sin aliases configurados.

## Flujo de cambio

1. Localizar la capa propietaria del comportamiento.
2. Mantener cada archivo Python por debajo de 130 líneas.
3. Añadir o actualizar una prueba enfocada.
4. Ejecutar `make test` y `make lint`.
5. Si cambia Compose, ejecutar `podman-compose config`.
6. Actualizar `README.md` o esta documentación si cambia un comando o una regla.
