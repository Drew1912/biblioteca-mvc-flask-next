# Biblioteca Console

Backend de consola con una interfaz TUI para la gestión de una biblioteca. Está organizado con una separación MVC: los modelos representan los datos, los controladores gestionan la navegación y las vistas dibujan tablas y paneles. Los casos de uso están separados por agregado dentro de `model/`.

## Desarrollo local

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
flask --app app:create_app init-db
make console
venv/bin/python -m flask --app app:create_app seed --reset
venv/bin/python -m flask --app app:create_app library materials create --type libro --title "Dune" --isbn "9780441172719" --copies 2
venv/bin/python -m flask --app app:create_app library readers create --name "Ana" --email "ana@example.com"
venv/bin/python -m flask --app app:create_app library materials list
venv/bin/python -m flask --app app:create_app library loans list
venv/bin/python -m flask --app app:create_app library materials update --id 1 --title "Dune: edición nueva"
venv/bin/python -m flask --app app:create_app library materials delete --id 1
pytest
```

La interfaz TUI muestra cinco gestiones: usuarios, lectores, materiales, préstamos y reportes. Puedes usar el mouse para pulsar botones, `Tab` o las flechas para cambiar el foco, `Enter` para activar una opción y `Escape` para volver.

## Estructura MVC

```text
app/
├── model/        # Material, Libro, Revista, Tesis, Persona y Prestamo
├── view/         # tablas y salida de consola
├── controllers/  # CLI dividido: users, readers, materials, loans, reports
├── settings/     # configuración de entorno
└── diagrama/     # diagrama de clases y tablas
```

Para ejecutar directamente con Flask, usa el intérprete del entorno virtual. No uses el comando `flask` global si el entorno no está activado:

```bash
venv/bin/python -m flask --app main:create_app console
```

La herencia del UML se representa así:

```text
Material -> Libro, Revista, Tesis
Persona  -> Administrador, Bibliotecario, Doctor, Estudiante
```

## PostgreSQL con Podman

Requiere Podman y `podman-compose`:

```bash
cp .env.example .env
podman-compose up --build
```

El servicio `db` usa PostgreSQL 16 y el servicio `app` muestra la ayuda de la CLI cuando termina de arrancar. Para ejecutar comandos contra PostgreSQL:

```bash
podman-compose run --rm app flask --app main:create_app init-db
podman-compose run --rm app flask --app main:create_app seed --reset
podman-compose run --rm app flask --app main:create_app library materials list
podman-compose run --rm app flask --app main:create_app console

La API queda disponible en `http://localhost:5000` y Next.js en `http://localhost:3000`. La web usa cookies de sesión HttpOnly y CORS restringido a `WEB_ORIGIN`.
```

La base de datos se conserva en el volumen `postgres_data`. Las credenciales de desarrollo están en `.env.example`; no se deben usar en producción.

## Documentación para el equipo

- [AGENTS.md](AGENTS.md): reglas obligatorias para futuras IAs y colaboradores.
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): capas, dependencias y persistencia.
- [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md): flujo de desarrollo y comandos.
- [docs/TESTING.md](docs/TESTING.md): cobertura y validaciones requeridas.
