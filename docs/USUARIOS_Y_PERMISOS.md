# Usuarios de desarrollo y permisos

## Acceso a la base actual

Comprobado el **7 de octubre de 2026** sobre PostgreSQL de Podman.
Esta lista corresponde a las **40 cuentas existentes**, todas activas.
Se verificó que la contraseña de desarrollo coincide con cada cuenta mediante
el método de comprobación de contraseñas del modelo, sin modificar sus datos.

- Web: http://localhost:3000/login
- Contraseña de las 40 cuentas: **`Biblioteca123!`**
- Son cuentas ficticias de desarrollo; no usar estas credenciales en producción.

Para probar un rol rápidamente:

| Rol | Correo | Contraseña |
|---|---|---|
| Administrador | `usuario03@test.local` | `Biblioteca123!` |
| Bibliotecario | `usuario01@test.local` | `Biblioteca123!` |
| Docente | `usuario02@test.local` | `Biblioteca123!` |
| Estudiante | `lector01@test.local` | `Biblioteca123!` |

Abre la web, introduce correo y contraseña y pulsa **Iniciar sesión**.
Para cambiar de usuario, pulsa **Cerrar sesión** y entra con otra cuenta.
En móvil, abre el menú para acceder a las gestiones y al cierre de sesión.

## Permisos de la web y API

Los permisos dependen del rol y se comprueban en Flask para cada operación.
Todas las cuentas de un mismo rol tienen los permisos de su columna.

| Operación | Administrador | Bibliotecario | Docente | Estudiante |
|---|---|---|---|---|
| Consultar y buscar libros, revistas y tesis | Sí | Sí | Sí | Sí |
| Consultar disponibilidad de materiales | Sí | Sí | Sí | Sí |
| Crear y editar materiales | Sí | Sí | No | No |
| Eliminar materiales sin historial | Sí | Sí | No | No |
| Consultar usuarios internos | Sí | Sí | No | No |
| Crear, editar y eliminar usuarios internos | Sí | No | No | No |
| Consultar lectores docentes y estudiantes | Sí | Sí | No | No |
| Crear, editar y eliminar lectores | Sí | No | No | No |
| Consultar préstamos | Todos | Todos | Solo propios | Solo propios |
| Registrar préstamos para personas | Sí | Sí | No | No |
| Registrar devoluciones | Sí | Sí | No | No |
| Consultar reportes de usuarios | Sí | Sí | No | No |
| Consultar reportes de lectores | Sí | Sí | No | No |
| Consultar inventario, préstamos, vencidos y resumen | Sí | Sí | No | No |
| Registrar cuentas desde `/auth/registro` | Sí | No | No | No |

### Condiciones de las operaciones

- **Usuarios** muestra administradores y bibliotecarios; **Lectores** muestra
  docentes y estudiantes. Todos heredan de Persona.
- Docentes y estudiantes consultan sus préstamos y vencimientos. Para solicitar
  un préstamo o registrar una devolución deben acudir al administrador o bibliotecario.
- No se eliminan materiales ni personas con historial de préstamos, aunque
  los préstamos ya estén devueltos. El administrador tampoco puede borrar su propia cuenta.
- El rol se elige al crear la cuenta. La edición permite modificar nombre,
  correo y carnet, pero no cambiar el rol ni la contraseña desde la web.
- Los préstamos no se editan ni se eliminan desde la web; se registra su devolución.
- El registro público está deshabilitado. Solo el administrador crea cuentas.
- La web exige sesión; las escrituras requieren origen válido y token CSRF.
- Hay un límite de diez intentos de login por minuto e IP. Si aparece el aviso
  de demasiados intentos, espera un minuto antes de volver a entrar.

## Todas las cuentas de la base actual

La contraseña común de todas las filas es **`Biblioteca123!`**.
Los ID sirven para identificar la cuenta desde la consola; para entrar en la web
se utiliza el correo. Los nombres y correos son ficticios.

### Administrador — 6 cuentas

| ID | Nombre | Correo | Estado |
|---|---|---|---|
| 23 | Usuario de prueba 03 | `usuario03@test.local` | Activo |
| 26 | Usuario de prueba 06 | `usuario06@test.local` | Activo |
| 29 | Usuario de prueba 09 | `usuario09@test.local` | Activo |
| 32 | Usuario de prueba 12 | `usuario12@test.local` | Activo |
| 35 | Usuario de prueba 15 | `usuario15@test.local` | Activo |
| 38 | Usuario de prueba 18 | `usuario18@test.local` | Activo |

### Bibliotecario — 7 cuentas

| ID | Nombre | Correo | Estado |
|---|---|---|---|
| 21 | Usuario de prueba 01 | `usuario01@test.local` | Activo |
| 24 | Usuario de prueba 04 | `usuario04@test.local` | Activo |
| 27 | Usuario de prueba 07 | `usuario07@test.local` | Activo |
| 30 | Usuario de prueba 10 | `usuario10@test.local` | Activo |
| 33 | Usuario de prueba 13 | `usuario13@test.local` | Activo |
| 36 | Usuario de prueba 16 | `usuario16@test.local` | Activo |
| 39 | Usuario de prueba 19 | `usuario19@test.local` | Activo |

### Docente — 7 cuentas

| ID | Nombre | Correo | Estado |
|---|---|---|---|
| 22 | Usuario de prueba 02 | `usuario02@test.local` | Activo |
| 25 | Usuario de prueba 05 | `usuario05@test.local` | Activo |
| 28 | Usuario de prueba 08 | `usuario08@test.local` | Activo |
| 31 | Usuario de prueba 11 | `usuario11@test.local` | Activo |
| 34 | Usuario de prueba 14 | `usuario14@test.local` | Activo |
| 37 | Usuario de prueba 17 | `usuario17@test.local` | Activo |
| 40 | Usuario de prueba 20 | `usuario20@test.local` | Activo |

### Estudiante — 20 cuentas

| ID | Nombre | Correo | Estado |
|---|---|---|---|
| 1 | Lector de prueba 01 | `lector01@test.local` | Activo |
| 2 | Lector de prueba 02 | `lector02@test.local` | Activo |
| 3 | Lector de prueba 03 | `lector03@test.local` | Activo |
| 4 | Lector de prueba 04 | `lector04@test.local` | Activo |
| 5 | Lector de prueba 05 | `lector05@test.local` | Activo |
| 6 | Lector de prueba 06 | `lector06@test.local` | Activo |
| 7 | Lector de prueba 07 | `lector07@test.local` | Activo |
| 8 | Lector de prueba 08 | `lector08@test.local` | Activo |
| 9 | Lector de prueba 09 | `lector09@test.local` | Activo |
| 10 | Lector de prueba 10 | `lector10@test.local` | Activo |
| 11 | Lector de prueba 11 | `lector11@test.local` | Activo |
| 12 | Lector de prueba 12 | `lector12@test.local` | Activo |
| 13 | Lector de prueba 13 | `lector13@test.local` | Activo |
| 14 | Lector de prueba 14 | `lector14@test.local` | Activo |
| 15 | Lector de prueba 15 | `lector15@test.local` | Activo |
| 16 | Lector de prueba 16 | `lector16@test.local` | Activo |
| 17 | Lector de prueba 17 | `lector17@test.local` | Activo |
| 18 | Lector de prueba 18 | `lector18@test.local` | Activo |
| 19 | Lector de prueba 19 | `lector19@test.local` | Activo |
| 20 | Lector de prueba 20 | `lector20@test.local` | Activo |

## Diferencia con una semilla nueva

Esta base conserva las cuentas anteriores: `usuario02@test.local` es docente
y `lector02@test.local` es estudiante. Las cuentas del rol retirado fueron
convertidas a docente conservando su correo, contraseña e historial.

En una base vacía creada con la semilla actual, la distribución es diferente:

| Cuentas | Rol en una semilla nueva |
|---|---|
| `usuario01`, `usuario04`, `usuario07`, `usuario10`, `usuario13`, `usuario16`, `usuario19` | Bibliotecario |
| Los otros `usuarioXX` del 01 al 20 | Administrador |
| `lectorXX` impares del 01 al 19 | Estudiante |
| `lectorXX` pares del 02 al 20 | Docente |

Todos esos correos terminan en `@test.local` y usan `Biblioteca123!`.
Para probar docente en una semilla nueva, utiliza `lector02@test.local`.

`make seed` conserva los datos existentes; no reasigna esos roles en una base ya
poblada. `seed --reset` borra los datos de desarrollo y los reemplaza: no hace falta
usarlo para probar las cuentas de este documento. Si se crean o eliminan cuentas,
esta lista debe actualizarse.

## Consola y TUI

CLI y TUI no requieren login ni aplican la matriz de permisos de la web.
Permiten la administración local a quien tenga acceso al entorno.

Para listar las cuentas actuales desde Podman:

```bash
podman-compose exec -T app flask --app app.main:create_app library users list
```

Para cambiar la contraseña de una cuenta ficticia desde consola, utiliza su ID
(reemplaza `23` por el ID deseado). Se solicita la nueva contraseña de forma oculta:

```bash
podman-compose exec app flask --app app.main:create_app library users password --id 23
```

Consulta también [Desarrollo](DEVELOPMENT.md), [Arquitectura y contratos](ARCHITECTURE.md)
y [Validaciones realizadas](TESTING.md).
