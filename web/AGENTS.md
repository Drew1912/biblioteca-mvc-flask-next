# Web

Aplican las reglas del AGENTS.md raíz. Usar pnpm y mantener pnpm-lock.yaml.
No usar npm ni crear package-lock.json. No introducir rutas de negocio Next.js.
Next.js exige `app/`; las responsabilidades propias van en model/controllers/view.
130 líneas como máximo por archivo fuente propio. Formularios con etiquetas,
loading/error/empty states, botones deshabilitados durante escrituras y foco visible.
No confiar en permisos del cliente: Flask es la autoridad.
Ejecutar `pnpm lint`, `pnpm build` y `pnpm test` desde este directorio.
