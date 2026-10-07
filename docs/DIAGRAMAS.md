# Diagramas y flujos del sistema Biblioteca

**Fecha de documentacion:** 07/10/2026

Este documento describe la implementacion actual. Los diagramas usan Mermaid y
pueden visualizarse en GitHub, VS Code con una extension Mermaid o cualquier
visor compatible.

## 1. Arquitectura general

```mermaid
flowchart LR
    U[Usuario] --> W[Next.js React]
    W -->|fetch + cookie + CSRF| A[Flask API /api/v1]
    A --> C[Controladores HTTP]
    C --> M[Servicios y entidades]
    M --> D[(PostgreSQL)]
    C --> S[Serializadores JSON]
    S --> W
```

## 2. Estructura MVC del backend

```mermaid
flowchart TD
    MAIN[app/main.py<br/>factoría Flask] --> HTTP[app/controllers/http_*.py]
    MAIN --> CLI[app/controllers/cli.py]
    HTTP --> SEC[seguridad, roles y CSRF]
    HTTP --> SERV[app/model/*.py<br/>servicios de negocio]
    CLI --> SERV
    TUI[controladores TUI] --> SERV
    SERV --> ORM[SQLAlchemy]
    ORM --> DB[(PostgreSQL o SQLite)]
    HTTP --> VIEW[app/view/serializers.py]
```

## 3. Diagrama entidad-relacion

```mermaid
erDiagram
    BIBLIOTECAS ||--o{ PERSONA : agrupa
    PERSONA ||--o{ PRESTAMO : recibe
    MATERIAL ||--o{ PRESTAMO : registra
    BIBLIOTECAS {
        int id PK
        string nombre
    }
    PERSONA {
        int id PK
        int biblioteca_id FK
        string tipo_persona
        string name
        string carnet_identidad UK
        string email UK
        boolean active
        string password_hash
    }
    MATERIAL {
        int id PK
        string tipo_material
        string title
        string isbn UK
        int total_copies
        int available_copies
    }
    PRESTAMO {
        int id PK
        int material_id FK
        int persona_id FK
        datetime loaned_at
        datetime due_at
        datetime returned_at
    }
```

## 4. Flujo de autenticacion

```mermaid
sequenceDiagram
    participant B as Navegador
    participant W as Next.js
    participant A as Flask API
    participant D as Base de datos
    B->>W: Abre /login
    W->>A: GET /auth/me
    A-->>W: CSRF y usuario nulo
    B->>W: Envia correo y contrasena
    W->>A: POST /auth/login + CSRF
    A->>D: Busca usuario activo
    D-->>A: Hash y rol
    A-->>W: Cookie HttpOnly + usuario + CSRF
    W-->>B: Dashboard segun rol
```

## 5. Flujo de una solicitud web

```mermaid
flowchart TD
    EVENTO[Accion en componente React] --> HOOK[use-library o formulario]
    HOOK --> API[web/model/api.ts]
    API -->|credentials include| ENDPOINT[API v1]
    ENDPOINT --> GUARD[Sesion, rol y CSRF]
    GUARD --> CTRL[Controlador HTTP]
    CTRL --> SERVICE[Servicio del modelo]
    SERVICE --> TX[transactional]
    TX --> DB[(Base de datos)]
    DB --> JSON[Serializer JSON]
    JSON --> STATE[Estado React]
    STATE --> UI[Vista actualizada]
```

## 6. Flujo de prestamos y devoluciones

```mermaid
flowchart TD
    INICIO[Administrador o bibliotecario] --> FORM[Formulario de prestamo]
    FORM --> VALIDAR{Material y persona validos?}
    VALIDAR -- No --> ERROR[Mostrar error]
    VALIDAR -- Si --> LOCK[Bloquear material en transaccion]
    LOCK --> COPIAS{Hay copias disponibles?}
    COPIAS -- No --> ERROR
    COPIAS -- Si --> CREATE[Crear Prestamo]
    CREATE --> DECREMENTAR[Disminuir available_copies]
    DECREMENTAR --> ACTIVO[Prestamo activo]
    ACTIVO --> DEVOLVER[Accion Devolver]
    DEVOLVER --> RETURN[Guardar returned_at]
    RETURN --> INCREMENTAR[Aumentar available_copies]
    INCREMENTAR --> HISTORIAL[Historial conservado]
```

## 7. Permisos por rol

```mermaid
flowchart TD
    REQUEST[Peticion API] --> SESSION{Sesion valida?}
    SESSION -- No --> 401[401 No autenticado]
    SESSION -- Si --> ROLE{Rol autorizado?}
    ROLE -- No --> 403[403 Prohibido]
    ROLE -- Si --> ACTION[Ejecutar servicio]
    ACTION --> RESULT[Respuesta JSON]
```

Administrador y bibliotecario gestionan materiales y prestamos. Solo el
administrador gestiona personas. Doctor y estudiante consultan el catalogo y
sus propios prestamos.

## 8. Estructura del frontend

```mermaid
flowchart TD
    APP[web/app/page.tsx] --> HOOK[web/controllers/use-library.ts]
    APP --> VIEWS[web/view/]
    VIEWS --> MATERIALS[materials.tsx]
    VIEWS --> USERS[users.tsx]
    VIEWS --> LOANS[loans.tsx]
    VIEWS --> REPORTS[reports.tsx]
    VIEWS --> FORM[form.tsx]
    HOOK --> CLIENT[web/model/api.ts]
    CLIENT --> API[Flask /api/v1]
    CSS[globals.css] --> APP
```

El layout es responsive: en movil aparece el menu hamburguesa, el contenido
ocupa el ancho disponible y el panel lateral se abre sobre la pagina.

## 9. Despliegue local

```mermaid
flowchart LR
    DEV[PowerShell] --> COMPOSE[docker compose up -d]
    COMPOSE --> DB[db<br/>PostgreSQL:5432]
    COMPOSE --> APP[app<br/>Flask:5000]
    COMPOSE --> WEB[web<br/>Next.js:3000]
    WEB -->|http://localhost:5000/api/v1| APP
    APP --> DB
```

## 10. Directorios clave

```text
app/main.py             Orquestacion Flask y configuracion
app/model/              Entidades, servicios, consultas y transacciones
app/controllers/        HTTP, CLI y TUI
app/view/               Serializacion y presentacion de consola
web/app/                Entradas Next.js y layout
web/model/              Cliente HTTP y contratos TypeScript
web/controllers/        Carga y estado del dashboard
web/view/                Componentes de presentacion
tests/                  Pruebas backend
web/tests/              Pruebas Playwright
docs/                   Documentacion y este generador
```
