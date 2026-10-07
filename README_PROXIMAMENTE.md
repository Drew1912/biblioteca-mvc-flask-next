# Mejoras proximas de Biblioteca

Este documento registra ideas para hacer el sistema mas funcional en futuras
etapas. No describe funcionalidades ya implementadas: cada propuesta debe
disenarse, desarrollarse y probarse antes de considerarse disponible.

## Estado actual

La version actual ya incluye:

- Frontend responsive con Next.js, React, Tailwind CSS y HeroUI.
- Login, logout, sesiones HttpOnly, CSRF y permisos por rol.
- Catalogo de materiales: libros, revistas y tesis.
- Gestion de personas, roles, materiales y prestamos.
- Registro de devoluciones e historial.
- Reportes de resumen, inventario, usuarios, prestamos y vencimientos.
- API Flask bajo `/api/v1`.
- PostgreSQL mediante Docker Compose y SQLite para pruebas locales.
- Pruebas backend, pruebas Playwright, lint y build.

Los roles actuales son administrador, bibliotecario, doctor y estudiante.
Doctor y estudiante pueden consultar el catalogo y sus propios prestamos. Los
prestamos los registran actualmente el administrador o el bibliotecario.

## Prioridad recomendada

El orden propuesto evita construir pantallas que dependan de contratos o reglas
de negocio que aun no existen.

1. Portal de autoservicio para solicitudes.
2. Disponibilidad y reglas de reservas.
3. Historial, notificaciones y experiencia del usuario.
4. Operacion diaria de la biblioteca.
5. Seguridad, auditoria y produccion.
6. Analitica, integraciones y accesibilidad avanzada.

## 1. Portal de autoservicio

Esta mejora queda aplazada, pero es la siguiente gran funcionalidad prevista.

### Para estudiantes y doctores

- Buscar y filtrar materiales desde el catalogo.
- Ver copias totales, copias disponibles y estado.
- Solicitar un prestamo o reservar un material.
- Consultar solicitudes propias.
- Cancelar una solicitud pendiente.
- Consultar prestamos activos e historial.
- Ver fechas limite y dias restantes.
- Recibir mensajes claros cuando no haya disponibilidad.

### Para bibliotecarios y administradores

- Ver solicitudes pendientes.
- Aprobar o rechazar solicitudes.
- Registrar un motivo de rechazo.
- Definir una fecha limite para recoger el material.
- Convertir una solicitud aprobada en prestamo.
- Marcar una solicitud como lista para recoger.
- Expirar solicitudes no recogidas.

### Cambios tecnicos necesarios

Se agregaria una entidad `SolicitudPrestamo`, sin borrar ni reemplazar
`prestamo`. Sus relaciones principales serian:

```text
persona 1 ---- N solicitud_prestamo
material 1 --- N solicitud_prestamo
solicitud 1 - 0..1 prestamo
```

Estados sugeridos:

```text
pendiente, aprobada, rechazada, lista_para_recoger,
cancelada, expirada
```

La devolucion seguiria perteneciendo a `prestamo`. Una migracion aditiva
crearia la tabla y sus indices. Antes de implementarla se deben decidir las
reglas de prioridad, la duracion de una reserva y si se aparta una copia al
aprobar o solamente al retirar el material.

Endpoints previstos:

```text
POST /api/v1/loan-requests
GET  /api/v1/loan-requests/mine
GET  /api/v1/loan-requests
POST /api/v1/loan-requests/:id/approve
POST /api/v1/loan-requests/:id/reject
POST /api/v1/loan-requests/:id/cancel
```

## 2. Catalogo y disponibilidad

- Busqueda por titulo, ISBN, tipo y autor cuando el modelo lo incorpore.
- Filtros combinables y ordenamiento.
- Paginacion para catalogos grandes.
- Vista detallada de cada material.
- Historial de disponibilidad.
- Cola de espera cuando no haya copias.
- Reglas configurables por tipo de usuario.
- Importacion de catalogo desde CSV validado.
- Exportacion controlada de inventario.

Para autores, categorias, ubicaciones y ejemplares fisicos se debe evaluar si
conviene ampliar el modelo actual o crear entidades nuevas. No se deben guardar
varios datos en una sola columna de texto si luego seran filtrables.

## 3. Experiencia del usuario

- Pagina de perfil para consultar y actualizar datos permitidos.
- Cambio de contrasena.
- Recuperacion de cuenta con flujo seguro.
- Indicador de sesiones activas.
- Preferencias de idioma y formato de fecha.
- Notificaciones dentro del sistema.
- Confirmaciones antes de acciones irreversibles.
- Estados vacios utiles y mensajes de error accionables.
- Mejoras de teclado, foco, contraste y lectores de pantalla.
- PWA opcional para consultar el catalogo desde movil.

No se deben guardar contrasenas ni tokens de sesion en `localStorage`.

## 4. Notificaciones

Cuando el portal de solicitudes exista, se podrian enviar notificaciones por:

- Solicitud recibida.
- Solicitud aprobada o rechazada.
- Material listo para recoger.
- Prestamo proximo a vencer.
- Prestamo vencido.
- Reserva expirada.

Primero se recomienda implementar notificaciones internas. El correo y otros
canales deben agregarse despues de definir proveedor, privacidad, reintentos,
preferencias del usuario y proteccion contra envios duplicados.

## 5. Operacion de la biblioteca

- Registro de ejemplares individuales con codigo de barras o QR.
- Escaneo para prestar y devolver.
- Inventario fisico y ubicacion de cada ejemplar.
- Estados de ejemplar: disponible, prestado, perdido, danado y mantenimiento.
- Renovacion de prestamos con reglas por rol.
- Multas o bloqueos configurables, si la institucion los requiere.
- Importacion y exportacion con validacion y vista previa.
- Acciones masivas con confirmacion y permisos.
- Panel de tareas pendientes para bibliotecarios.

Estas funciones requieren definir primero las reglas institucionales. El sistema
no debe inventar multas, limites o sanciones sin una decision del negocio.

## 6. Reportes y analitica

- Reportes filtrables por periodo, material y rol.
- Prestamos mas frecuentes.
- Materiales nunca utilizados.
- Tasa de devoluciones tardias.
- Tiempo promedio de prestamo.
- Demanda no atendida y materiales en espera.
- Exportacion CSV y PDF con permisos.
- Graficos accesibles y tablas descargables.
- Registro del momento de generacion del reporte.

Los reportes deben consultar servicios del modelo y no realizar consultas desde
los componentes de presentacion.

## 7. Seguridad y administracion

- Auditoria de inicios de sesion y acciones administrativas.
- Registro de aprobaciones, rechazos, ediciones y devoluciones.
- Politicas de contrasena configurables.
- Recuperacion segura de cuenta.
- Rotacion de secretos y configuracion por entorno.
- Limitador de login compartido al usar varios procesos.
- HTTPS, cookies `Secure` y cabeceras de seguridad en produccion.
- Backups automaticos de PostgreSQL y prueba de restauracion.
- Migraciones versionadas antes de cualquier cambio de esquema productivo.
- Reglas de retencion y eliminacion de datos personales.

Nunca se deben incluir contrasenas de desarrollo en una instalacion productiva.

## 8. Calidad, rendimiento y despliegue

- Pruebas de concurrencia de prestamos y devoluciones en PostgreSQL.
- Pruebas de migracion desde bases antiguas.
- Pruebas de carga para catalogo y reportes.
- Healthchecks de base, API y frontend.
- Logs estructurados sin contrasenas ni datos sensibles.
- Metricas de errores, latencia y disponibilidad.
- CI para lint, pruebas, build y Playwright.
- Imagenes Docker reproducibles y escaneo de dependencias.
- Entornos separados para desarrollo, pruebas y produccion.
- Despliegue con HTTPS y dominio real cuando corresponda.

## Criterio para iniciar cada mejora

Antes de implementar una mejora se debe documentar:

1. Regla de negocio y roles autorizados.
2. Cambios necesarios en la base de datos.
3. Contrato HTTP y respuestas de error.
4. Cambios de frontend y estados de carga.
5. Pruebas de backend, frontend y permisos.
6. Migracion y plan de rollback si cambia el esquema.
7. Actualizacion de la documentacion correspondiente.

La mejora solo se considerara terminada cuando pase las validaciones del
proyecto y no deje errores conocidos sin documentar.
