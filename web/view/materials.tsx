"use client";
import { useState } from "react";
import { Material } from "../model/api";
import { DeleteButton, Editor, Field } from "./form";
export function Materials({ items, manage, reload }: { items: Material[]; manage: boolean; reload: () => void }) {
  const [query, setQuery] = useState("");
  const [editing, setEditing] = useState<Material | "new" | null>(null);
  const existing = editing && editing !== "new" ? editing : null;
  const fields: Field[] = [{ name: "title", label: "Título", value: existing?.title },
    { name: "isbn", label: "ISBN / Código", value: existing?.isbn }];
  if (!existing) fields.push({ name: "type", label: "Tipo", value: "libro",
    options: ["libro", "revista", "tesis"].map(value => ({ value, label: value })) },
    { name: "copies", label: "Copias", type: "number", value: 1, min: 1 });
  const filtered = items.filter(x => `${x.title} ${x.isbn} ${x.type}`.toLowerCase().includes(query.toLowerCase()));
  return <section className="panel catalog-panel"><div className="toolbar"><div><span className="section-kicker">Colección</span><h2>Catálogo de materiales</h2></div>
    {manage && <button className="primary" aria-label="Nuevo material" onClick={() => setEditing("new")}>+ Nuevo material</button>}</div>
    <label className="search-field"><span aria-hidden="true">⌕</span><input aria-label="Buscar por título, tipo o ISBN" placeholder="Buscar por título, tipo o ISBN…" value={query} onChange={e => setQuery(e.target.value)} /></label>
    {editing && <Editor key={existing?.id ?? "new"} title={existing ? "Editar material" : "Nuevo material"}
      path={`/materials${existing ? `/${existing.id}` : ""}`} method={existing ? "PATCH" : "POST"}
      fields={fields} done={() => { setEditing(null); reload(); }} cancel={() => setEditing(null)} />}
    <table className="table"><thead><tr><th>Título</th><th>Tipo</th><th>ISBN</th><th>Disponibilidad</th>{manage && <th>Acciones</th>}</tr></thead>
      <tbody>{filtered.map(x => <tr key={x.id}><td>{x.title}</td><td><span className="pill">{x.type}</span></td>
        <td className="muted-cell">{x.isbn}</td><td><span className={x.availableCopies ? "availability available" : "availability unavailable"}>{x.availableCopies ? `${x.availableCopies} disponibles` : "Agotado"}</span><small className="copies">{x.availableCopies} de {x.totalCopies} copias</small></td>{manage && <td className="actions">
          <button onClick={() => setEditing(x)}>Editar</button><DeleteButton path={`/materials/${x.id}`} done={reload} /></td>}</tr>)}</tbody></table>
    {!filtered.length && <p>No hay materiales para esta búsqueda.</p>}
  </section>;
}
