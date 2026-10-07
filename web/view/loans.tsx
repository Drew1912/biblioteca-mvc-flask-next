"use client";
import { useState } from "react";
import { api, Loan, Material, User } from "../model/api";
import { Editor } from "./form";
export function Loans({ items, materials, users, manage, reload }: {
  items: Loan[]; materials: Material[]; users: User[]; manage: boolean; reload: () => void;
}) {
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [filter, setFilter] = useState("todos");
  const status = (x: Loan) => x.returnedAt ? "Devuelto" : new Date(x.dueAt) < new Date() ? "Vencido" : "Activo";
  async function returnLoan(id: number) {
    setBusy(true); setError("");
    try { await api(`/loans/${id}/return`, { method: "POST" }); reload(); }
    catch (reason) { setError(reason instanceof Error ? reason.message : "Error"); }
    finally { setBusy(false); }
  }
  const filtered = items.filter(x => filter === "todos" || status(x) === filter);
  return <section className="panel catalog-panel"><div className="toolbar"><div><span className="section-kicker">Actividad</span><h2>{manage ? "Préstamos" : "Mis préstamos"}</h2></div>
    {manage && <button className="primary" aria-label="Nuevo préstamo" onClick={() => setCreating(true)}>+ Nuevo préstamo</button>}</div>
    <label className="filter-field">Estado<select value={filter} onChange={e => setFilter(e.target.value)}>
      {["todos", "Activo", "Vencido", "Devuelto"].map(x => <option key={x}>{x}</option>)}</select></label>
    {creating && <Editor title="Registrar préstamo" path="/loans" method="POST" cancel={() => setCreating(false)}
      done={() => { setCreating(false); reload(); }} fields={[
        { name: "materialId", label: "Material disponible", options: materials.filter(x => x.availableCopies > 0)
          .map(x => ({ value: x.id, label: `${x.title} · ${x.isbn}` })) },
        { name: "personId", label: "Persona", options: users.filter(x => x.active).map(x => ({ value: x.id, label: `${x.name} · ${x.email}` })) },
        { name: "days", label: "Días", type: "number", value: 14, min: 1 },
      ]} />}
    {error && <p role="alert" className="error">{error}</p>}
    <table className="table"><thead><tr><th>Material</th><th>Persona</th><th>Fecha de vencimiento</th><th>Estado</th>{manage && <th>Acciones</th>}</tr></thead>
      <tbody>{filtered.map(x => <tr key={x.id}><td>{x.material.title}</td><td>{x.user.name}</td>
        <td className="muted-cell">{new Date(x.dueAt).toLocaleDateString("es-BO", { day: "2-digit", month: "short", year: "numeric" })}</td><td><span className={`pill loan-status ${status(x).toLowerCase()}`}>{status(x)}</span></td>
        {manage && <td>{!x.returnedAt && <button className="action-button" aria-label="Devolver" disabled={busy} onClick={() => returnLoan(x.id)}>Marcar devolución</button>}</td>}</tr>)}</tbody></table>
    {!filtered.length && <p>No hay préstamos en este estado.</p>}
  </section>;
}
