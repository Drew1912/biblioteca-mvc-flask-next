"use client";
import { FormEvent, useState } from "react";
import { api } from "../model/api";
export type Field = { name: string; label: string; type?: string; value?: string | number;
  options?: { value: string | number; label: string }[]; min?: number; required?: boolean };
export function Editor({ title, path, method, fields, done, cancel }: {
  title: string; path: string; method: string; fields: Field[]; done: () => void; cancel: () => void;
}) {
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setBusy(true); setError("");
    const payload = Object.fromEntries(new FormData(event.currentTarget));
    try { await api(path, { method, body: JSON.stringify(payload) }); done(); }
    catch (reason) { setError(reason instanceof Error ? reason.message : "Error"); }
    finally { setBusy(false); }
  }
  return <form className="editor" onSubmit={submit}><h3>{title}</h3><div className="form-grid">
    {fields.map(field => <label className="field" key={field.name}>{field.label}
      {field.options ? <select name={field.name} defaultValue={field.value} required={field.required !== false}>
        <option value="">Seleccionar…</option>{field.options.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
      </select> : <input name={field.name} type={field.type ?? "text"} defaultValue={field.value}
        required={field.required !== false}
        min={field.min} maxLength={field.type === "email" ? 254 : 120} minLength={field.type === "password" ? 12 : undefined} />}
    </label>)}
  </div>{error && <p role="alert" className="error">{error}</p>}
    <button className="primary" disabled={busy}>{busy ? "Guardando…" : "Guardar"}</button>{" "}
    <button type="button" disabled={busy} onClick={cancel}>Cancelar</button>
  </form>;
}
export function DeleteButton({ path, done }: { path: string; done: () => void }) {
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  async function remove() {
    if (!window.confirm("¿Eliminar este registro? Esta operación no se puede deshacer.")) return;
    setBusy(true); setError("");
    try { await api(path, { method: "DELETE" }); done(); }
    catch (reason) { setError(reason instanceof Error ? reason.message : "Error"); }
    finally { setBusy(false); }
  }
  return <><button className="danger" disabled={busy} onClick={remove}>Eliminar</button>
    {error && <p role="alert" className="error">{error}</p>}</>;
}
