# Web

Aplican las reglas del AGENTS.md raíz. Usar pnpm y mantener pnpm-lock.yaml.
No usar npm ni crear package-lock.json. No introducir rutas de negocio Next.js.
Next.js exige `app/`; las responsabilidades propias van en model/controllers/view.
130 líneas como máximo por archivo fuente propio. Formularios con etiquetas,
loading/error/empty states, botones deshabilitados durante escrituras y foco visible.
No confiar en permisos del cliente: Flask es la autoridad.
Ejecutar `pnpm lint`, `pnpm build` y `pnpm test` desde este directorio.

<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->
