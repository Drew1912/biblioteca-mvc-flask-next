"use client";
import { useEffect, useRef } from "react";
import type { Section, User } from "../model/contracts";

const icons: Record<Section, string> = {
  overview: "◫", materials: "▤", users: "♙", readers: "♧", loans: "⇄", reports: "▥",
};
export function Navigation({ user, section, labels, open, setOpen, select, logout, busy }: {
  user: User; section: Section; labels: Partial<Record<Section, string>>; open: boolean;
  setOpen: (open: boolean) => void; select: (section: Section) => void; logout: () => void; busy: boolean;
}) {
  const toggle = useRef<HTMLButtonElement>(null);
  useEffect(() => {
    if (!open) return;
    function escape(event: KeyboardEvent) {
      if (event.key === "Escape") { setOpen(false); toggle.current?.focus(); }
    }
    document.addEventListener("keydown", escape);
    return () => document.removeEventListener("keydown", escape);
  }, [open, setOpen]);
  return <>
    <button ref={toggle} className="menu-toggle" aria-label={open ? "Cerrar menú" : "Abrir menú"}
      aria-expanded={open} aria-controls="navegacion" onClick={() => setOpen(!open)}><span /><span /><span /></button>
    {open && <button className="menu-overlay" aria-label="Cerrar fondo del menú" onClick={() => setOpen(false)} />}
    <aside id="navegacion" className={`sidebar${open ? " is-open" : ""}`}>
      <div className="brand"><span className="brand-symbol" aria-hidden="true">▤</span> Biblioteca
        <small>Un espacio para aprender</small></div>
      <div><span className="nav-caption">MI ESPACIO</span><nav className="nav" aria-label="Navegación principal">
        {Object.entries(labels).map(([id, label]) => <button key={id} aria-label={label}
          aria-current={section === id ? "page" : undefined} className={section === id ? "active" : ""}
          onClick={() => select(id as Section)}><span aria-hidden="true">{icons[id as Section]}</span>{label}</button>)}
      </nav></div>
      <div className="sidebar-note"><span aria-hidden="true">✧</span><p>Cada lectura abre<br />una nueva posibilidad.</p></div>
      <div className="sidebar-footer"><div className="identity">{user.name}<small>{user.role}</small></div>
        <button className="logout" disabled={busy} onClick={logout}>{busy ? "Saliendo…" : "Cerrar sesión"}</button></div>
    </aside>
  </>;
}
