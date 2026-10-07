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
  const [menuOpen, setMenuOpen] = useState(false);
  const [error, setError] = useState("");
  const { user, materials, loans, users, summary, load } = data;
  if (!user) return <main className="login"><div className="login-card loading-card" aria-live="polite">
    {data.error ? <><p role="alert" className="error">{data.error}</p><button className="primary" onClick={load}>Reintentar</button></> :
      <><span className="loading-spinner" aria-hidden="true" /><p role="status">Cargando biblioteca…</p></>}
  </div></main>;
  const manage = ["administrador", "bibliotecario"].includes(user.role);
  const labels: Record<string, string> = { overview: "Resumen", materials: "Catálogo", loans: "Préstamos",
    ...(manage ? { users: "Personas y roles", reports: "Reportes" } : {}) };
  async function logout() {
    try { await api("/auth/logout", { method: "POST" }); window.location.assign("/login"); }
    catch (reason) { setError(reason instanceof Error ? reason.message : "Error"); }
  }
  const stats = manage ? summary : { materiales: materials.length, prestamos_activos: loans.filter(x => !x.returnedAt).length };
  const statLabels: Record<string, string> = {
    materiales: "Materiales registrados", prestamos_activos: "Préstamos activos",
    prestamos: "Préstamos totales", usuarios: "Personas registradas",
  };
  function selectSection(id: string) {
    setSection(id);
    setMenuOpen(false);
  }
  return <div className="shell"><button className="menu-toggle" aria-label="Abrir menú" aria-expanded={menuOpen}
      onClick={() => setMenuOpen(open => !open)}><span /><span /><span /></button>
    {menuOpen && <button className="menu-overlay" aria-label="Cerrar menú" onClick={() => setMenuOpen(false)} />}
    <aside className={`sidebar${menuOpen ? " is-open" : ""}`}><div className="brand">Biblioteca<small>Conocimiento a tu alcance</small></div>
    <nav className="nav" aria-label="Navegación principal">{Object.entries(labels).map(([id, label]) =>
      <button key={id} aria-current={section === id ? "page" : undefined} className={section === id ? "active" : ""}
        onClick={() => selectSection(id)}>{label}</button>)}</nav>
    <div className="sidebar-footer"><div className="identity">{user.name}<small>{user.role}</small></div>
      <button className="logout" onClick={logout}>Cerrar sesión</button></div></aside>
    <main className="main"><header className="page-header"><div><span className="eyebrow">Tu biblioteca virtual</span><h1 className="heading">{labels[section]}</h1></div>
      <div className="profile-chip"><span className="avatar">{user.name.charAt(0).toUpperCase()}</span><span>{user.name}</span></div>
    </header>
      {(error || data.error) && <p role="alert" className="error">{error || data.error}</p>}
      {section === "overview" && <><div className="hero"><span className="hero-kicker">Buenos días, {user.name.split(" ")[0]}</span><h2>Tu próxima lectura<br />empieza aquí.</h2>
        <p>Explora el catálogo y consulta tus préstamos.</p><button className="primary" onClick={() => selectSection("materials")}>Explorar catálogo →</button></div>
        <div className="stats">{Object.entries(stats).map(([label, value]) => <div className="stat" key={label}>
          <span className="stat-icon" aria-hidden="true">✦</span><b>{value}</b><span>{statLabels[label] ?? label.replaceAll("_", " ")}</span></div>)}</div></>}
      {section === "materials" && <Materials items={materials} manage={manage} reload={load} />}
      {section === "loans" && <Loans items={loans} materials={materials} users={users} manage={manage} reload={load} />}
      {section === "users" && manage && <Users items={users} admin={user.role === "administrador"} self={user.id} reload={load} />}
      {section === "reports" && manage && <Reports />}
    </main></div>;
}
