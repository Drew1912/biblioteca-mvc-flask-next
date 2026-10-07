"use client";
import { useDashboard } from "../controllers/use-dashboard";
import type { Section } from "../model/contracts";
import { Materials } from "./materials";
import { Users } from "./users";
import { Loans } from "./loans";
import { Reports } from "./reports";
import { Overview } from "./overview";
import { Navigation } from "./navigation";

export function Dashboard() {
  const data = useDashboard();
  const { user, materials, loans, users, summary, load, section, manage, labels, selectSection } = data;
  if (!user) return <main className="login"><div className="login-card loading-card" aria-live="polite">
    {data.error ? <><p role="alert" className="error">{data.error}</p>
      <button className="primary" onClick={load}>Reintentar</button></> :
      <><span className="loading-spinner" aria-hidden="true" /><p role="status">Cargando biblioteca…</p></>}
  </div></main>;
  const staff = users.filter(person => ["administrador", "bibliotecario"].includes(person.role));
  const readers = users.filter(person => ["docente", "estudiante"].includes(person.role));
  return <div className="shell">
    <a href="#contenido" className="skip-link">Saltar al contenido</a>
    <Navigation user={user} section={section} labels={labels} open={data.menuOpen}
      setOpen={data.setMenuOpen} select={selectSection} logout={data.logout} busy={data.session.busy} />
    <main id="contenido" className="main" tabIndex={-1}>
      <header className="page-header"><div><span className="eyebrow">Biblioteca · {user.role}</span>
        <h1 className="heading">{labels[section]}</h1></div>
        <div className="profile-chip"><span className="avatar">{user.name.charAt(0).toUpperCase()}</span>
          <span>{user.name}<small>{user.role}</small></span></div>
      </header>
      {(data.session.error || data.error) && <div role="alert" className="error">
        {data.session.error || data.error} <button disabled={data.loading} onClick={load}>Reintentar</button>
      </div>}
      {data.loading && <p role="status" className="refresh-status">Actualizando biblioteca…</p>}
      {section === "overview" && <Overview user={user} materials={materials} loans={loans}
        summary={summary} manage={manage} select={selectSection} />}
      {section === "materials" && <Materials items={materials} manage={manage} reload={load} />}
      {section === "loans" && <Loans items={loans} materials={materials} users={users} manage={manage} reload={load} />}
      {(["users", "readers"] as Section[]).includes(section) && manage &&
        <Users key={section} group={section === "readers" ? "readers" : "staff"}
          items={section === "readers" ? readers : staff} admin={user.role === "administrador"}
          self={user.id} reload={load} />}
      {section === "reports" && manage && <Reports />}
      <footer className="page-footer">Biblioteca · Libros, revistas y tesis</footer>
    </main>
  </div>;
}
