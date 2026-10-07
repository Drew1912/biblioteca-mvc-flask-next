"use client";
import { FormEvent } from "react";
import { useMutation } from "../controllers/use-mutation";
export type Field = { name: string; label: string; type?: string; value?: string | number;
  options?: { value: string | number; label: string }[]; min?: number; required?: boolean };
export function Editor({ title, path, method, fields, done, cancel }: {
  title: string; path: string; method: string; fields: Field[]; done: () => void; cancel: () => void;
}) {
  const { error, busy, mutate } = useMutation();
  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const payload = Object.fromEntries(new FormData(event.currentTarget));
    void mutate(path, method, payload, done);
  }
  return <form className="editor" onSubmit={submit}><h3>{title}</h3><div className="form-grid">
    {fields.map(field => <label className="field" key={field.name}>{field.label}
      {field.options ? <select disabled={busy} name={field.name} defaultValue={field.value} required={field.required !== false}>
        <option value="">Seleccionar…</option>{field.options.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
      </select> : <input disabled={busy} name={field.name} type={field.type ?? "text"} defaultValue={field.value}
        required={field.required !== false}
        min={field.min} maxLength={field.type === "email" ? 254 : 120} minLength={field.type === "password" ? 12 : undefined} />}
    </label>)}
  </div>{error && <p role="alert" className="error">{error}</p>}
    <button className="primary" disabled={busy}>{busy ? "Guardando…" : "Guardar"}</button>{" "}
    <button type="button" disabled={busy} onClick={cancel}>Cancelar</button>
  </form>;
}
export function DeleteButton({ path, done }: { path: string; done: () => void }) {
  const { error, busy, mutate } = useMutation();
  function remove() {
    if (window.confirm("¿Eliminar este registro? Esta operación no se puede deshacer.")) {
      void mutate(path, "DELETE", undefined, done);
    }
  }
  return <><button className="danger" disabled={busy} onClick={remove}>Eliminar</button>
    {error && <p role="alert" className="error">{error}</p>}</>;
}
