"use client";
import { useState } from "react";
import { User } from "../model/api";
import { DeleteButton, Editor } from "./form";
import { userFields } from "./user-fields";
export function Users({ items, admin, self, reload }: { items: User[]; admin: boolean; self: number; reload: () => void }) {
  const [editing, setEditing] = useState<User | "new" | null>(null);
  const [query, setQuery] = useState("");
  const existing = editing && editing !== "new" ? editing : null;
  const fields = userFields(existing);
  const filtered = items.filter(x => `${x.name} ${x.email} ${x.role}`.toLowerCase().includes(query.toLowerCase()));
  return <section className="panel"><div className="toolbar"><h2>Personas y roles</h2>
    {admin && <button className="primary" onClick={() => setEditing("new")}>Nuevo usuario</button>}</div>
    <label className="field">Buscar persona<input value={query} onChange={e => setQuery(e.target.value)} /></label>
    {editing && <Editor key={existing?.id ?? "new"} title={existing ? "Editar usuario" : "Nuevo usuario"}
      path={`/users${existing ? `/${existing.id}` : ""}`} method={existing ? "PATCH" : "POST"} fields={fields}
      done={() => { setEditing(null); reload(); }} cancel={() => setEditing(null)} />}
    <table className="table"><thead><tr><th>Nombre</th><th>Correo</th><th>Rol</th><th>Estado</th>{admin && <th>Acciones</th>}</tr></thead>
      <tbody>{filtered.map(x => <tr key={x.id}><td>{x.name}</td><td>{x.email}</td><td><span className="pill">{x.role}</span></td>
        <td>{x.active ? "Activo" : "Inactivo"}</td>{admin && <td className="actions"><button onClick={() => setEditing(x)}>Editar</button>
          {x.id !== self && <DeleteButton path={`/users/${x.id}`} done={reload} />}</td>}</tr>)}</tbody></table>
    {!filtered.length && <p>No hay personas para esta búsqueda.</p>}
  </section>;
}
