# Reglas obligatorias para agentes

## Alcance autorizado

Biblioteca tiene Flask, CLI, TUI Textual, PostgreSQL y un proyecto Next.js en
`web/`, solicitado explícitamente. Usar pnpm exclusivamente para la web.
No sustituir ni eliminar cambios locales ajenos. Leer `docs/ARCHITECTURE.md`,
`docs/DEVELOPMENT.md` y `docs/TESTING.md` antes de modificar comportamientos.

## Arquitectura MVC

- `app/main.py`: único orquestador, configuración y instancia SQLAlchemy.
- `app/model/`: entidades, consultas, servicios, transacciones, reportes y semilla.
- `app/controllers/`: adaptadores CLI, TUI y HTTP separados por responsabilidad.
- `app/view/`: presentación y serialización sin consultas ni persistencia.
- `web/app/`: entradas obligatorias de Next.js, layout y estilos.
- `web/model/`: contratos de datos y cliente HTTP.
- `web/controllers/`: coordinación de carga y estado.
- `web/view/`: componentes de presentación y formularios.
- `tests/`: pruebas Python; `web/tests/`: pruebas de navegador.
- `docs/` y `diagrama/`: documentación, no capas de aplicación.

Dentro de `app/` solo se permiten las carpetas `model`, `controllers`, `view`.
No recrear `api/`, `settings/`, `extensions.py` ni un `main.py` en la raíz.
El prefijo HTTP `/api/v1` es una URL, no una carpeta ni una capa adicional.
No concentrar gestiones en el orquestador ni duplicar modelos en Next.js.

## Código

Máximo 130 líneas físicas por archivo fuente propio, incluidos tests y estilos.
No comprimir código para evadir el límite: dividir por responsabilidad.
Los lockfiles y artefactos generados no son código fuente propio.
Una función tiene una responsabilidad. El modelo es dueño del negocio y SQL.
Los servicios mutantes usan `transactional`: commit al terminar, rollback al fallar.
Usar `datetime.now(UTC)`. Mantener nombres públicos consistentes con la API.
No introducir imports sin uso, código muerto, secretos ni comentarios narrativos.

## Interacción y seguridad

La consola y TUI no requieren login. Mantener mouse, foco, Tab, flechas, Enter
Escape y Select para entidades existentes.
La web requiere sesión HttpOnly; nunca almacenar credenciales en localStorage.
Toda escritura exige CSRF y validación del origen. CORS admite un origen explícito.
Los permisos se validan en Flask, no solo ocultando botones.
Administrador: materiales, personas, préstamos y reportes.
Bibliotecario: materiales, préstamos, consulta de personas y reportes.
Docente y estudiante: catálogo y únicamente sus propios préstamos.
No borrar materiales/personas con historial ni permitir autoborrado web.
Los errores deben ser visibles; no dejar pantallas cargando indefinidamente.

## Datos y validación

Semilla solo de desarrollo: mínimo 20 materiales, 20 lectores, 20 usuarios
internos y 20 préstamos. `seed --reset` borra datos de desarrollo explícitamente.
No usar datos ni credenciales reales. Semilla deshabilitada en producción.

Antes de finalizar cualquier cambio ejecutar `make test` y `make lint`.
Para cambios web: `make web-build` y `make web-test`.
Para Podman/PostgreSQL: `podman-compose config` y `make build`, más prueba real
cuando sea posible. No afirmar que una validación pasó si no se ejecutó.
Documentar limitaciones del entorno y errores pendientes; no declarar terminado
un cambio con fallos conocidos. Actualizar documentación al cambiar contratos.
