# Diagrama de clases

```mermaid
classDiagram
    class Material {
        +int id
        +string title
        +string isbn
        +int total_copies
        +int available_copies
    }
    class Libro
    class Revista
    class Tesis
    Material <|-- Libro
    Material <|-- Revista
    Material <|-- Tesis

    class Persona {
        +int id
        +string name
        +string email
        +bool active
    }
    class Administrador
    class Bibliotecario
    class Doctor
    class Estudiante
    Persona <|-- Administrador
    Persona <|-- Bibliotecario
    Persona <|-- Doctor
    Persona <|-- Estudiante

    class Prestamo {
        +int id
        +datetime loaned_at
        +datetime due_at
        +datetime returned_at
    }
    Material "1" --> "0..*" Prestamo
    Persona "1" --> "0..*" Prestamo
```

## Tablas

- `material`: tabla base con discriminador `tipo_material`.
- `persona`: tabla base con discriminador `tipo_persona`.
- `prestamo`: relaciona `material_id` y `persona_id`, y conserva el historial de devoluciones.

La herencia usa el patrón single-table inheritance de SQLAlchemy: las subclases comparten la tabla de su clase base y el discriminador identifica el tipo concreto.
