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
  return <section className="panel catalog-panel"><div className="toolbar"><div><span className="section-kicker">Comunidad</span><h2>Personas y roles</h2></div>
    {admin && <button className="primary" aria-label="Nuevo usuario" onClick={() => setEditing("new")}>+ Nuevo usuario</button>}</div>
    <label className="search-field"><span aria-hidden="true">⌕</span><input aria-label="Buscar persona" placeholder="Buscar por nombre, correo o rol…" value={query} onChange={e => setQuery(e.target.value)} /></label>
    {editing && <Editor key={existing?.id ?? "new"} title={existing ? "Editar usuario" : "Nuevo usuario"}
      path={`/users${existing ? `/${existing.id}` : ""}`} method={existing ? "PATCH" : "POST"} fields={fields}
      done={() => { setEditing(null); reload(); }} cancel={() => setEditing(null)} />}
    <table className="table"><thead><tr><th>Persona</th><th>Correo</th><th>Carnet</th><th>Rol</th><th>Estado</th>{admin && <th>Acciones</th>}</tr></thead>
      <tbody>{filtered.map(x => <tr key={x.id}><td><span className="person-cell"><span className="person-avatar">{x.name.charAt(0).toUpperCase()}</span>{x.name}</span></td><td className="muted-cell">{x.email}</td><td className="muted-cell">{x.carnetIdentity}</td><td><span className="pill">{x.role}</span></td>
        <td><span className={x.active ? "status-dot active" : "status-dot inactive"}>{x.active ? "Activo" : "Inactivo"}</span></td>{admin && <td className="actions"><button onClick={() => setEditing(x)}>Editar</button>
          {x.id !== self && <DeleteButton path={`/users/${x.id}`} done={reload} />}</td>}</tr>)}</tbody></table>
    {!filtered.length && <p>No hay personas para esta búsqueda.</p>}
  </section>;
}
