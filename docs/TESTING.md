# Validación

## Backend y estructura

```bash
make test
make lint
venv/bin/python -m pytest --cov=app --cov-report=term-missing
```

La suite usa SQLite temporal: dominio, CRUD, rollback tras duplicados,
disponibilidad, devoluciones, semilla, CLI, navegación Textual, login/logout,
CSRF, origen, CORS, límite de login, permisos de los cuatro roles, aislamiento de
préstamos y errores de payload. Verifica MVC y máximo de 130 líneas físicas.
`make lint` ejecuta compilación Python, Ruff, estructura y TypeScript.

## Web real y PostgreSQL

```bash
pnpm --dir web install --frozen-lockfile
pnpm --dir web exec playwright install chromium
make web-build
podman-compose config
make build
make up
podman-compose exec -T app flask --app app.main:create_app seed
make web-test
```

Playwright usa Chromium y los servicios reales en localhost:3000 y localhost:5000.
La semilla debe tener las cuentas ficticias documentadas. Las pruebas crean y
eliminan registros propios de materiales/personas y agregan un préstamo con
devolución: ejecutarlas sobre una base de desarrollo. `seed` sin reset conserva
los datos existentes; no borra una base para acomodar una prueba.

La suite E2E comprueba login, CRUD, préstamo/devolución, reportes, permisos de los
cuatro roles, logout, credenciales inválidas y viewport móvil. Conserva trazas
al fallar en `web/test-results/`. `E2E_BASE_URL` permite cambiar la dirección web.
Para repetir muchas veces, esperar el intervalo del limitador de login.

## Alcance

Un build exitoso no reemplaza pruebas de navegador. SQLite no prueba los bloqueos
concurrentes de PostgreSQL. Las suites actuales no constituyen auditoría externa
de seguridad, prueba de carga ni garantía de ausencia total de errores.
Antes de escalar a múltiples procesos configurar un almacén compartido del
limitador y validar concurrencia con PostgreSQL.

## Suite sobre PostgreSQL aislado

```bash
podman-compose exec -T db createdb -U biblioteca biblioteca_test
TEST_DATABASE_URL=postgresql+psycopg://biblioteca:biblioteca@localhost:5432/biblioteca_test make test
```

El fixture solo admite PostgreSQL si la base se llama `biblioteca_test`: crea y
borra sus tablas. La prueba de concurrencia hace dos préstamos y dos devoluciones
simultáneas; solo una operación de cada par puede modificar la disponibilidad.
En SQLite esa prueba se omite deliberadamente.
