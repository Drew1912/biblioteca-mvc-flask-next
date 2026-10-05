# Reglas del proyecto

## Alcance

Biblioteca es un backend Flask de consola con TUI Textual y PostgreSQL. No agregar frontend web, rutas HTTP ni dependencias de Next.js salvo solicitud explícita.

## Arquitectura obligatoria

- `app/model/`: entidades SQLAlchemy, servicios de dominio, reportes y seed.
- `app/view/`: presentación de consola reutilizable.
- `app/controllers/`: entrada CLI y TUI; coordina, no contiene reglas de negocio.
- `app/settings/`: configuración por entorno.
- `tests/`: pruebas de dominio, CLI y TUI.
- `diagrama/`: documentación del modelo y relaciones.

Los controladores deben permanecer divididos por responsabilidad. No volver a concentrar gestiones en un único archivo.

## Clean code

- Ningún archivo Python de aplicación debe superar 130 líneas.
- Una función debe tener una responsabilidad clara.
- La lógica de persistencia y negocio pertenece a `app/model/`, no al TUI.
- Los nombres públicos y comandos deben estar en español funcional o mantener consistencia con la API existente.
- No duplicar adaptadores, modelos o configuraciones.
- Usar transacciones y hacer rollback ante errores de persistencia.
- Preferir `datetime.now(UTC)` para fechas nuevas.
- No introducir código muerto, imports sin uso ni comentarios narrativos.

## TUI

- Usar Textual para interacción real con teclado y mouse.
- Preferir `Select` para elegir entidades existentes; no pedir IDs cuando una etiqueta legible sea posible.
- Mantener navegación con foco, `Enter`, `Escape`, `Tab` y flechas.
- Las pantallas solo coordinan y muestran; invocan servicios del modelo.

## Datos de prueba

- `seed --reset` debe ser reproducible y seguro para desarrollo.
- La semilla debe mantener como mínimo 20 materiales, 20 lectores, 20 usuarios de sistema y 20 préstamos.
- No usar datos reales ni credenciales reales.

## Validación obligatoria

Antes de terminar cualquier cambio:

```bash
make test
make lint
```

Si cambia Podman o PostgreSQL:

```bash
make build
podman-compose config
```

No finalizar con pruebas fallidas o errores de compilación.
