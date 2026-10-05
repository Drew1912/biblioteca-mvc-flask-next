# Pruebas

## Suite

```bash
make test
```

La suite cubre:

- creación, actualización y eliminación de materiales;
- herencia de materiales y personas;
- disponibilidad, préstamo y devolución;
- duplicados de email desde CLI;
- reportes y datos de prueba;
- navegación TUI con teclado;
- combos Textual para seleccionar material y persona.

## Semilla

```bash
venv/bin/python -m flask --app app:create_app seed --reset
```

La salida esperada incluye 20 materiales, 40 personas y 20 préstamos. `--reset` solo se debe usar en desarrollo o pruebas porque borra los datos actuales.

## Validación estructural

```bash
make lint
find app tests -type f -name '*.py' -print0 | xargs -0 wc -l | sort -nr
```

Ningún módulo de aplicación debe superar 130 líneas. Si un archivo crece, dividirlo por responsabilidad antes de añadir más lógica.

## Base de datos

Las pruebas usan SQLite temporal para ser rápidas y aisladas. PostgreSQL se valida con Podman cuando cambia configuración, conexiones o SQL específico:

```bash
podman-compose config
make build
```
