"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { api, User } from "../../../model/api";
import { Editor } from "../../../view/form";
import { userFields } from "../../../view/user-fields";

export default function RegistrationPage() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [created, setCreated] = useState(false);

  useEffect(() => {
    let active = true;
    api<{ user: User | null }>("/auth/me")
      .then(data => { if (active) setUser(data.user); })
      .catch(reason => { if (active) setError(reason.message); })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, []);

  return <main className="login"><section className="login-card">
    <span className="eyebrow">Biblioteca virtual</span>
    <h1>Registro de usuarios</h1>
    {loading ? <p role="status">Comprobando sesión…</p> : error ?
      <><p role="alert" className="error">{error}</p>
        <button onClick={() => window.location.reload()}>Reintentar</button></> :
      user?.role === "administrador" ? created ?
        <p role="status">Usuario registrado correctamente.</p> :
        <Editor title="Nuevo usuario" path="/users" method="POST" fields={userFields()}
          done={() => setCreated(true)} cancel={() => window.location.assign("/")} /> :
        <p>El registro de cuentas lo realiza un administrador de la biblioteca.
          Solicita tu cuenta al administrador o inicia sesión con una cuenta autorizada.</p>}
    <p><Link href={user ? "/" : "/login"}>{user ? "Volver al panel" : "Iniciar sesión"}</Link></p>
  </section></main>;
}
