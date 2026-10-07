# Desarrollo

## Entorno local

Requiere Python 3.11+, Node 22 y pnpm 10.11.0.

```bash
python -m venv venv
make install
pnpm --dir web install --frozen-lockfile
make init-db
make seed
python -m flask --app app.main:create_app run --port 5000
# En otra terminal:
pnpm --dir web dev
```

Sin DATABASE_URL, Flask usa SQLite local en `instance/`. Web: http://localhost:3000.
API: http://localhost:5000/api/v1. Usar el mismo hostname en ambos servicios;
no mezclar localhost con 127.0.0.1 porque las cookies dependen del host.

La semilla crea 20 materiales, 20 lectores (10 docentes y 10 estudiantes),
20 usuarios internos (administradores y bibliotecarios) y 20 préstamos.
Cuentas ficticias: `usuario03@test.local` (administrador), `usuario01@test.local`
(bibliotecario), `lector02@test.local` (docente), `lector01@test.local` (estudiante).
Contraseña de desarrollo para todas: `Biblioteca123!`. No publicarlas en producción.

Consulta [Usuarios y permisos](USUARIOS_Y_PERMISOS.md) para ver las 40 cuentas
de la base actual, las credenciales y los permisos detallados de cada rol.

## Consola

```bash
make console
python -m flask --app app.main:create_app library --help
```

No requiere login. Navegar con teclado y mouse; seleccionar entidades por etiqueta.

## Docker Compose

```bash
docker compose config
make build
make up
docker compose exec app flask --app app.main:create_app seed --reset
```

`make up` crea tablas, no borra datos ni ejecuta reset. La semilla es explícita.
PostgreSQL persiste en volumen. `make down` conserva el volumen.
`make console` ejecuta localmente; para el contenedor usar:
`docker compose exec app flask --app app.main:create_app console`.

El `Makefile` usa Docker Compose por defecto y funciona en Windows, Linux y
macOS. En Windows detecta `venv\Scripts\python.exe`; si no existe, usa
`python`. En Linux y macOS detecta `venv/bin/python`; si no existe, usa
`python3`. Para usar Podman de forma explícita:

```bash
make COMPOSE=podman-compose build
make COMPOSE=podman-compose up
```

Para regenerar la documentación visual después de editar la plantilla:

```powershell
python docs\generar_diagramas.py
```

Las versiones PNG de los diagramas están en `docs\diagramas-png\`. Se generan
con un renderizador local de Mermaid y se conservan como documentación estática.

Variables en `.env.example`: DATABASE_URL, SECRET_KEY, WEB_ORIGIN,
NEXT_PUBLIC_API_URL, SESSION_COOKIE_SECURE y APP_ENV. La URL pública de API se
incorpora durante build de Next.js: reconstruir web si cambia. CORS debe coincidir
con el origen del navegador, no con el nombre interno del contenedor.

Antes de publicar: establecer SECRET_KEY aleatorio, APP_ENV=production,
SESSION_COOKIE_SECURE=1, HTTPS en el proxy y credenciales propias de PostgreSQL.
La configuración Compose incluida es para desarrollo local.

## Cambios

Leer AGENTS.md y arquitectura; modificar la capa dueña del comportamiento,
añadir pruebas de regresión y ejecutar las validaciones documentadas.
No commitear `.env`, bases de datos, node_modules ni artefactos generados.

`init-db` actualiza de forma aditiva bases antiguas sin `password_hash`.
`seed` sin reset habilita contraseñas solo para las cuentas ficticias originales
que coinciden por nombre/correo y aún no tienen hash; conserva las demás cuentas.

Para habilitar acceso web a una cuenta creada desde consola, usar
`flask --app app.main:create_app library users password --id ID`.
La contraseña se solicita de forma oculta y con confirmación.

La ruta `/auth/registro` permite al administrador registrar usuarios con el
mismo formulario del panel. Sin sesión o con otro rol muestra instrucciones
para solicitar una cuenta. No existe autorregistro público.

Las cuentas preexistentes del rol retirado pasan a docente al iniciar la aplicación,
sin cambiar sus correos ni contraseñas. Las credenciales anteriores corresponden
a una semilla nueva. `seed` sin `--reset` conserva las cuentas existentes.
En la web, Usuarios gestiona personal interno; Lectores gestiona docentes y
estudiantes. El registro por URL permite crear cualquiera de los cuatro roles.

Reportes desde CLI: `flask --app app.main:create_app library reports --type readers`.
Los tipos disponibles son summary, inventory, users, readers, loans y overdue.
Para crear un docente desde consola: `library readers create --name "Docente de
prueba" --email docente@test.local --role docente` (anteponer el comando Flask).
`make seed` conserva los datos; el borrado exige invocar `seed --reset` explícitamente.
