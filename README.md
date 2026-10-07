# Biblioteca MVC

Gestión de biblioteca con Flask, PostgreSQL, consola/TUI Textual y web Next.js.
El orquestador es `app/main.py`; las únicas capas backend son model, controllers
y view. La consola no exige login; la web aplica permisos por rol.

## Iniciar el sistema con Docker Desktop

### Requisitos

- Docker Desktop abierto y en estado `Running`.
- Git y PowerShell disponibles.
- El proyecto descargado en esta carpeta:
  `C:\Users\usser\Downloads\biblioteca-mvc-flask-next-main_oficial\biblioteca-mvc-flask-next-main`

### Arranque normal

Después de encender el equipo, abre Docker Desktop y espera a que termine de
iniciar. Luego abre una terminal de PowerShell y ejecuta:

```powershell
cd "C:\Users\usser\Downloads\biblioteca-mvc-flask-next-main_oficial\biblioteca-mvc-flask-next-main"
docker compose up -d
docker compose ps
```

Debes ver tres servicios:

- `db`: PostgreSQL, puerto `5432`.
- `app`: backend Flask, puerto `5000`.
- `web`: frontend Next.js, puerto `3000`.

La base de datos se inicializa automáticamente al arrancar el backend. Los
datos guardados en PostgreSQL permanecen en el volumen `postgres_data`.

### Abrir la aplicación

Cuando los tres servicios estén activos, abre:

- Aplicación web: http://localhost:3000
- API: http://localhost:5000
- Estado de la API: http://localhost:5000/api/v1/health

El healthcheck debe mostrar:

```json
{"status":"ok"}
```

Inicia sesión con una cuenta de desarrollo de la sección
[Credenciales de desarrollo](#credenciales-de-desarrollo).

### Si es la primera instalación o quieres datos de prueba

Para crear los datos ficticios iniciales:

```powershell
docker compose exec app flask --app app.main:create_app seed --reset
```

Este comando crea materiales, personas y préstamos de prueba. `--reset` borra
los datos actuales de desarrollo, por lo que solo debe usarse en una base de
pruebas.

### Detener y volver a iniciar

Para detener los servicios sin borrar el volumen de PostgreSQL:

```powershell
docker compose down
```

Para iniciarlos otra vez:

```powershell
docker compose up -d
```

No uses `docker compose down -v` salvo que quieras borrar también los datos de
PostgreSQL.

### Ver logs y diagnosticar

```powershell
docker compose ps
docker compose logs -f
docker compose logs -f app
docker compose logs -f web
```

Si un puerto está ocupado, cierra otro servidor que use `3000`, `5000` o
`5432` y vuelve a ejecutar `docker compose up -d`.

### Aplicar cambios de código

Si modificas únicamente el frontend:

```powershell
docker compose up -d --build web
```

Si modificas únicamente el backend:

```powershell
docker compose up -d --build app
```

Si modificas ambos:

```powershell
docker compose up -d --build
```

También puedes reconstruir con Make:

```powershell
make build
make up
```

### Usar el botón de Docker Desktop

También puedes abrir el proyecto desde Docker Desktop y pulsar el botón de
inicio del proyecto `biblioteca-mvc-flask-next-main`. La terminal es preferible
porque muestra los errores y confirma el estado de cada servicio.

## Inicio alternativo con Podman

```bash
make COMPOSE=podman-compose build
make COMPOSE=podman-compose up
podman-compose exec app flask --app app.main:create_app seed --reset
```

Abre http://localhost:3000. Cuenta ficticia de administrador:
`usuario03@test.local` / `Biblioteca123!` (solo desarrollo).
`seed --reset` elimina datos existentes: usar únicamente en una base de prueba.

## Credenciales de desarrollo

La lista completa de cuentas de la base actual y sus permisos está en
[Usuarios y permisos](docs/USUARIOS_Y_PERMISOS.md).

La semilla crea cuentas ficticias para probar cada rol. Todas usan la
contraseña `Biblioteca123!`:

| Rol           | Correo                 | Contraseña       |
| ------------- | ---------------------- | ---------------- |
| Administrador | `usuario03@test.local` | `Biblioteca123!` |
| Bibliotecario | `usuario01@test.local` | `Biblioteca123!` |
| Docente        | `lector02@test.local` | `Biblioteca123!` |
| Estudiante    | `lector01@test.local`  | `Biblioteca123!` |

También se crean las cuentas `usuario04@test.local` a
`usuario20@test.local` y `lector02@test.local` a `lector20@test.local`.
Las cuentas `usuarioXX` son administradores o bibliotecarios. Los lectores
`lectorXX` alternan entre estudiantes (impares) y docentes (pares). Los datos, nombres, correos y contraseñas son exclusivamente
de prueba: no usar estas credenciales ni `seed --reset` en producción.

## Validar

```bash
make test
make lint
make web-build
make web-test
docker compose config
```

- [Reglas para IAs](AGENTS.md)
- [Arquitectura y permisos](docs/ARCHITECTURE.md)
- [Instalación, cuentas de prueba y ejecución local](docs/DEVELOPMENT.md)
- [Pruebas y limitaciones](docs/TESTING.md)
- [Diagrama de clases](diagrama/clases.md)
- [Diagramas y flujos completos](docs/DIAGRAMAS.md)
- [Plantilla de diagramas](docs/DIAGRAMAS_PLANTILLA.md)

La web incluye búsqueda, alta/edición/eliminación de materiales y personas según
rol, préstamos, devoluciones y reportes. Docente y estudiante solo consultan el
catálogo y sus préstamos. Se conserva el historial de préstamos.

En bases anteriores migradas, la cuenta `usuario02@test.local` conserva su correo
pero ahora es **docente**; `lector02@test.local` sigue siendo estudiante. En una
semilla nueva se usan los roles de la tabla anterior. No es necesario borrar datos.

El panel separa **Usuarios**, **Lectores**, **Catálogo**, **Préstamos** y **Reportes**.
Usuarios contiene administradores y bibliotecarios; Lectores contiene docentes y
estudiantes. Hay reportes independientes para ambas gestiones, inventario,
préstamos y vencidos. Las escrituras web validan sesión, rol, origen y CSRF en Flask.
