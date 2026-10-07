"use client";

import Link from "next/link";
import { useState } from "react";
import { useSession } from "../controllers/use-session";
import { Editor } from "./form";
import { userFields } from "./user-fields";

export function RegistrationPage() {
  const { user, loading, error } = useSession();
  const [created, setCreated] = useState(false);

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
