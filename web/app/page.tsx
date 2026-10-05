"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api, Loan, Material, User } from "../lib/api";

type Summary = { materiales: number; copias_disponibles: number; usuarios: number; prestamos_activos: number; prestamos_vencidos: number };

type Section = "overview" | "materials" | "loans" | "users" | "reports";

export default function Dashboard() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [section, setSection] = useState<Section>("overview");
  const [summary, setSummary] = useState<Summary | null>(null);
  const [materials, setMaterials] = useState<Material[]>([]);
  const [loans, setLoans] = useState<Loan[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [error, setError] = useState("");
  const [showMaterialForm, setShowMaterialForm] = useState(false);

  async function load() {
    try {
      const me = await api<{ user: User | null }>("/auth/me");
      if (!me.user) return router.push("/login");
      setUser(me.user);
      const [stats, materialData, loanData] = await Promise.all([
        api<Summary>("/reports/summary"), api<{ items: Material[] }>("/materials"), api<{ items: Loan[] }>("/loans"),
      ]);
      setSummary(stats); setMaterials(materialData.items); setLoans(loanData.items);
      if (["administrador", "bibliotecario"].includes(me.user.role)) setUsers((await api<{ items: User[] }>("/users")).items);
    } catch (reason) { setError(reason instanceof Error ? reason.message : "No se pudo cargar la información"); }
  }
  useEffect(() => { load(); }, []);
  async function logout() { await api("/auth/logout", { method: "POST" }); router.push("/login"); }
  if (!user || !summary) return <main className="login"><div className="login-card">Cargando biblioteca...</div></main>;
  const canManage = ["administrador", "bibliotecario"].includes(user.role);
  return <div className="shell"><aside className="sidebar"><div className="brand">Biblioteca<small>Centro de gestión</small></div><nav className="nav">
    {(["overview", "materials", "loans", ...(canManage ? ["users", "reports"] : [])] as Section[]).map((item) => <button className={section === item ? "active" : ""} key={item} onClick={() => setSection(item)}>{labels[item]}</button>)}
  </nav><button className="logout" onClick={logout}>Cerrar sesión</button></aside>
  <main className="main"><span className="eyebrow">Panel operativo</span><h1 className="heading">Hola, {user.name}</h1>{error && <div className="error">{error}</div>}
    {section === "overview" && <Overview summary={summary} loans={loans} />}{section === "materials" && <Materials items={materials} canManage={canManage} showForm={showMaterialForm} onToggleForm={() => setShowMaterialForm(!showMaterialForm)} onCreated={load} />}{section === "loans" && <Loans items={loans} canManage={canManage} onReturned={load} />}{section === "users" && <Users items={users} />}{section === "reports" && <Reports summary={summary} />}
  </main></div>;
}
const labels: Record<Section, string> = { overview: "Resumen", materials: "Materiales", loans: "Préstamos", users: "Usuarios", reports: "Reportes" };
function Overview({ summary, loans }: { summary: Summary; loans: Loan[] }) { return <><div className="stats">{[[summary.materiales, "Materiales"], [summary.copias_disponibles, "Copias disponibles"], [summary.usuarios, "Usuarios"], [summary.prestamos_vencidos, "Vencidos"]].map(([value, label]) => <div className="stat" key={label}><b>{value}</b><span>{label}</span></div>)}</div><div className="panel"><h2>Préstamos recientes</h2><Loans items={loans.slice(0, 5)} /></div></>; }
function Materials({ items, canManage, showForm, onToggleForm, onCreated }: { items: Material[]; canManage: boolean; showForm: boolean; onToggleForm: () => void; onCreated: () => void }) { return <div className="panel"><div className="toolbar"><h2>Catálogo de materiales</h2>{canManage && <button className="primary" onClick={onToggleForm}>{showForm ? "Cerrar" : "Nuevo material"}</button>}</div>{showForm && <MaterialForm onCreated={onCreated} /> }<table className="table"><thead><tr><th>Tipo</th><th>Título</th><th>ISBN</th><th>Disponibilidad</th></tr></thead><tbody>{items.map((item) => <tr key={item.id}><td><span className="pill">{item.type}</span></td><td>{item.title}</td><td>{item.isbn}</td><td>{item.availableCopies}/{item.totalCopies}</td></tr>)}</tbody></table></div>; }
function MaterialForm({ onCreated }: { onCreated: () => void }) { const [form, setForm] = useState({ type: "libro", title: "", isbn: "", copies: "1" }); const [message, setMessage] = useState(""); async function submit(event: React.FormEvent) { event.preventDefault(); try { await api("/materials", { method: "POST", body: JSON.stringify({ ...form, copies: Number(form.copies) }) }); setMessage("Material creado"); onCreated(); } catch (reason) { setMessage(reason instanceof Error ? reason.message : "Error"); } } return <form className="toolbar" onSubmit={submit}><select value={form.type} onChange={(event) => setForm({ ...form, type: event.target.value })}><option value="libro">Libro</option><option value="revista">Revista</option><option value="tesis">Tesis</option></select><input required placeholder="Título" value={form.title} onChange={(event) => setForm({ ...form, title: event.target.value })} /><input required placeholder="ISBN" value={form.isbn} onChange={(event) => setForm({ ...form, isbn: event.target.value })} /><input required min="1" type="number" value={form.copies} onChange={(event) => setForm({ ...form, copies: event.target.value })} /><button className="primary">Guardar</button><span>{message}</span></form>; }
function Loans({ items, canManage, onReturned }: { items: Loan[]; canManage: boolean; onReturned: () => void }) { async function returnLoan(id: number) { await api(`/loans/${id}/return`, { method: "POST" }); onReturned(); } return <table className="table"><thead><tr><th>Material</th><th>Persona</th><th>Vence</th><th>Estado</th><th /></tr></thead><tbody>{items.map((item) => <tr key={item.id}><td>{item.material.title}</td><td>{item.user.name}</td><td>{new Date(item.dueAt).toLocaleDateString("es")}</td><td><span className="pill">{item.returnedAt ? "Devuelto" : "Activo"}</span></td><td>{canManage && !item.returnedAt && <button className="danger" onClick={() => returnLoan(item.id)}>Devolver</button>}</td></tr>)}</tbody></table>; }
function Users({ items }: { items: User[] }) { return <div className="panel"><h2>Personas y roles</h2><table className="table"><thead><tr><th>Nombre</th><th>Correo</th><th>Rol</th><th>Estado</th></tr></thead><tbody>{items.map((item) => <tr key={item.id}><td>{item.name}</td><td>{item.email}</td><td><span className="pill">{item.role}</span></td><td>{item.active ? "Activo" : "Inactivo"}</td></tr>)}</tbody></table></div>; }
function Reports({ summary }: { summary: Summary }) { return <div className="panel"><h2>Reporte general</h2><table className="table"><tbody>{Object.entries(summary).map(([key, value]) => <tr key={key}><td>{key.replaceAll("_", " ")}</td><td>{value}</td></tr>)}</tbody></table></div>; }
