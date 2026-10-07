"use client";
import { useState } from "react";
import { useReport } from "../controllers/use-report";
const reports = { inventory: "Inventario", users: "Usuarios internos", readers: "Lectores por rol", loans: "Préstamos", overdue: "Vencidos" };
export function Reports() {
  const [type, setType] = useState("inventory");
  const { rows, error, loading } = useReport(type);
  const headers: Record<string, string[]> = {
    inventory: ["Tipo", "Título", "ISBN", "Copias", "Disponibles"], users: ["Rol", "Nombre", "Correo", "Estado"],
    readers: ["Rol", "Nombre", "Correo", "Estado"],
    loans: ["Material", "Persona", "Vence", "Estado"],
    overdue: ["Material", "Persona", "Vence", "Días de retraso"],
  };
  return <section className="panel catalog-panel"><div className="reports-heading"><div><span className="section-kicker">Análisis</span><h2>Reportes</h2><p>Consulta el estado de tu biblioteca.</p></div><span className="report-mark" aria-hidden="true">▥</span></div><label className="filter-field">Selecciona un reporte
    <select aria-label="Reporte" value={type} onChange={e => setType(e.target.value)}>{Object.entries(reports).map(([id, label]) =>
      <option key={id} value={id}>{label}</option>)}</select></label>
    {error ? <p role="alert" className="error">No se pudo cargar el reporte: {error}</p> : loading ? <p className="loading-state">Cargando reporte…</p> :
      <><table className="table"><thead><tr>{headers[type].map(h => <th key={h}>{h}</th>)}</tr></thead>
        <tbody>{rows.map((row, i) => <tr key={i}>{row.map((cell, j) => <td key={j}>{String(cell ?? "—")}</td>)}</tr>)}</tbody></table>
        {!rows.length && <p>No hay registros.</p>}</>}
  </section>;
}
