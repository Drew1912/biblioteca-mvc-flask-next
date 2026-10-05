# Biblioteca MVC

Gestión de biblioteca con Flask, PostgreSQL, consola/TUI Textual y web Next.js.
El orquestador es `app/main.py`; las únicas capas backend son model, controllers
y view. La consola no exige login; la web aplica permisos por rol.

## Iniciar con Podman

```bash
make build
make up
podman-compose exec app flask --app app.main:create_app seed --reset
```

Abrir http://localhost:3000. Cuenta ficticia de administrador:
`usuario03@test.local` / `Biblioteca123!` (solo desarrollo).
`seed --reset` elimina datos existentes: usar únicamente en una base de prueba.

## Validar

```bash
make test
make lint
make web-build
make web-test
podman-compose config
```

- [Reglas para IAs](AGENTS.md)
- [Arquitectura y permisos](docs/ARCHITECTURE.md)
- [Instalación, cuentas de prueba y ejecución local](docs/DEVELOPMENT.md)
- [Pruebas y limitaciones](docs/TESTING.md)
- [Diagrama de clases](diagrama/clases.md)

La web incluye búsqueda, alta/edición/eliminación de materiales y personas según
rol, préstamos, devoluciones y reportes. Doctor y estudiante solo consultan el
catálogo y sus préstamos. Se conserva el historial de préstamos.
