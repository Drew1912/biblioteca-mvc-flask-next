import type { User } from "../model/api";
import type { Field } from "./form";

export function userFields(existing: User | null = null, group?: "staff" | "readers"): Field[] {
  const roles = group === "staff" ? ["bibliotecario", "administrador"] :
    group === "readers" ? ["estudiante", "docente"] : ["estudiante", "docente", "bibliotecario", "administrador"];
  const fields: Field[] = [
    { name: "name", label: "Nombre", value: existing?.name },
    { name: "email", label: "Correo", type: "email", value: existing?.email },
    { name: "documento_identidad", label: "Carnet de identidad", value: existing?.carnetIdentity, required: false },
  ];
  if (!existing) {
    fields.push({
      name: "role", label: "Rol",
      options: roles.map(value => ({ value, label: value })),
    }, { name: "password", label: "Contraseña (mínimo 12 caracteres)", type: "password" });
  }
  return fields;
}
