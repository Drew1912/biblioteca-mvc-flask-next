# Validación

## Backend y estructura

```bash
make test
make lint
venv/bin/python -m pytest --cov=app --cov-report=term-missing
```

La suite usa SQLite temporal: dominio, CRUD, rollback tras duplicados,
disponibilidad, devoluciones, semilla, CLI, navegación Textual, login/logout,
CSRF, origen obligatorio, CORS, límite de login, permisos de los cuatro roles, aislamiento de
préstamos y errores de payload. Verifica MVC y máximo de 130 líneas físicas.
`make lint` ejecuta compilación Python, Ruff, estructura y TypeScript.

## Web real y PostgreSQL

```bash
pnpm --dir web install --frozen-lockfile
pnpm --dir web exec playwright install chromium
make web-build
podman-compose config
make COMPOSE=podman-compose build
make COMPOSE=podman-compose up
podman-compose exec -T app flask --app app.main:create_app seed
make web-test
```

Playwright usa Chromium y los servicios reales en localhost:3000 y localhost:5000.
La semilla debe tener las cuentas ficticias documentadas. Las pruebas crean y
eliminan registros propios de materiales/personas y agregan un préstamo con
devolución: ejecutarlas sobre una base de desarrollo. `seed` sin reset conserva
los datos existentes; no borra una base para acomodar una prueba.

La suite E2E comprueba login, CRUD de usuarios y lectores, préstamo/devolución, reportes separados, permisos de los
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

## Roles y base existente

Para una semilla nueva, Playwright utiliza `lector02@test.local` como docente.
En una base antigua migrada, usar
`E2E_TEACHER_EMAIL=usuario02@test.local make web-test` para verificar esa cuenta
conservando el historial. No ejecutar reset para acomodar las pruebas.
La suite incluye búsqueda por tipo/disponibilidad, menú móvil con Escape,
separación de usuarios/lectores y recuperación tras un fallo de conexión.
Los préstamos creados por E2E conservan su historial; las altas temporales sin
préstamos se eliminan. Respetar el límite de diez logins/minuto al repetir la suite.

## Ejecución verificada — 7 de octubre de 2026

| Validación ejecutada | Resultado |
|---|---|
| `make test` con SQLite | 61 aprobadas; 1 omitida por requerir bloqueos PostgreSQL |
| `TEST_DATABASE_URL=postgresql+psycopg://biblioteca:biblioteca@localhost:5432/biblioteca_test make test` | 62 aprobadas, incluida concurrencia |
| `make lint` | Compilación Python, Ruff, siete reglas de arquitectura y TypeScript aprobados |
| `make web-build` | Build de producción Next.js aprobado |
| `podman-compose config` | Configuración válida |
| `make COMPOSE=podman-compose build` | Imágenes Flask y Next.js construidas |
| `E2E_TEACHER_EMAIL=usuario02@test.local make web-test` | 10 pruebas Chromium aprobadas sobre los contenedores y PostgreSQL reales |

Los servicios quedaron activos en localhost:3000 (web), localhost:5000 (API) y
localhost:5432 (PostgreSQL). `/api/v1/health` respondió `{"status":"ok"}`.
Se conservaron el volumen y los registros anteriores; `seed` se ejecutó sin reset.
Las pruebas PostgreSQL usaron únicamente la base aislada `biblioteca_test`.

Cuentas verificadas mediante login en navegador sobre esta base migrada:

| Rol | Correo |
|---|---|
| Administrador | `usuario03@test.local` |
| Bibliotecario | `usuario01@test.local` |
| Docente | `usuario02@test.local` |
| Estudiante | `lector01@test.local` |

Contraseña ficticia de desarrollo para las cuatro: `Biblioteca123!`.
Playwright guarda capturas del panel de administrador y del estudiante en móvil
en los subdirectorios correspondientes de `web/test-results/`.

La reorganización Python se comprueba además con reglas de arquitectura que
exigen las cuatro gestiones en `app/controllers`, impiden `db.session` en
controladores y vistas y mantienen el máximo de 130 líneas. CLI, TUI y HTTP
utilizan los nuevos imports `app.controllers.materiales`, `usuarios`, `personas`
y `prestamos`; los métodos de modelo conservan validación, SQL y transacciones.
