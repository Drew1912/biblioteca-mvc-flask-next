"use client";
import { useState } from "react";
import { api } from "../model/api";
import { useLibrary } from "../controllers/use-library";
import { Materials } from "../view/materials";
import { Users } from "../view/users";
import { Loans } from "../view/loans";
import { Reports } from "../view/reports";
export default function Dashboard() {
  const data = useLibrary();
  const [section, setSection] = useState("overview");
  const [error, setError] = useState("");
  const { user, materials, loans, users, summary, load } = data;
  if (!user) return <main className="login"><div className="login-card">
    {data.error ? <><p role="alert">{data.error}</p><button onClick={load}>Reintentar</button></> : "Cargando biblioteca…"}
  </div></main>;
  const manage = ["administrador", "bibliotecario"].includes(user.role);
  const labels: Record<string, string> = { overview: "Resumen", materials: "Catálogo", loans: "Préstamos",
    ...(manage ? { users: "Personas y roles", reports: "Reportes" } : {}) };
  async function logout() {
    try { await api("/auth/logout", { method: "POST" }); window.location.assign("/login"); }
    catch (reason) { setError(reason instanceof Error ? reason.message : "Error"); }
  }
  const stats = manage ? summary : { materiales: materials.length, prestamos_activos: loans.filter(x => !x.returnedAt).length };
  return <div className="shell"><aside className="sidebar"><div className="brand">Biblioteca<small>Conocimiento a tu alcance</small></div>
    <nav className="nav" aria-label="Navegación principal">{Object.entries(labels).map(([id, label]) =>
      <button key={id} aria-current={section === id ? "page" : undefined} className={section === id ? "active" : ""}
        onClick={() => setSection(id)}>{label}</button>)}</nav>
    <div className="identity">{user.name}<small>{user.role}</small></div><button className="logout" onClick={logout}>Cerrar sesión</button></aside>
    <main className="main"><span className="eyebrow">Tu biblioteca virtual</span><h1 className="heading">{labels[section]}</h1>
      {(error || data.error) && <p role="alert" className="error">{error || data.error}</p>}
      {section === "overview" && <><div className="hero"><span>Un lugar para descubrir</span><h2>Tu próxima lectura<br />empieza aquí.</h2>
        <p>Explora el catálogo y consulta tus préstamos.</p><button className="primary" onClick={() => setSection("materials")}>Explorar catálogo →</button></div>
        <div className="stats">{Object.entries(stats).map(([label, value]) => <div className="stat" key={label}>
          <b>{value}</b><span>{label.replaceAll("_", " ")}</span></div>)}</div></>}
      {section === "materials" && <Materials items={materials} manage={manage} reload={load} />}
      {section === "loans" && <Loans items={loans} materials={materials} users={users} manage={manage} reload={load} />}
      {section === "users" && manage && <Users items={users} admin={user.role === "administrador"} self={user.id} reload={load} />}
      {section === "reports" && manage && <Reports />}
    </main></div>;
}
