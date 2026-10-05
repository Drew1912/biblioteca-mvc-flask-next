import type { User } from "../model/api";
import type { Field } from "./form";

export function userFields(existing: User | null = null): Field[] {
  const fields: Field[] = [
    { name: "name", label: "Nombre", value: existing?.name },
    { name: "email", label: "Correo", type: "email", value: existing?.email },
  ];
  if (!existing) {
    fields.push({
      name: "role", label: "Rol",
      options: ["estudiante", "doctor", "bibliotecario", "administrador"]
        .map(value => ({ value, label: value })),
    }, { name: "password", label: "Contraseña (mínimo 12 caracteres)", type: "password" });
  }
  return fields;
}
