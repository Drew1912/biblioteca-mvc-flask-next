"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { useMutation } from "../controllers/use-mutation";

export function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { error, busy: loading, mutate } = useMutation();

  async function submit(event: FormEvent) {
    event.preventDefault();
    await mutate("/auth/login", "POST", { email, password }, () => router.push("/"));
  }

  return <main className="login"><form className="login-card" onSubmit={submit}>
    <span className="eyebrow">Biblioteca virtual</span>
    <h1>Bienvenido</h1><p>Accede al centro de gestión de tu biblioteca.</p>
    <label className="field">Correo<input type="email" autoComplete="username" required value={email} onChange={(event) => setEmail(event.target.value)} /></label>
    <label className="field">Contraseña<input type="password" autoComplete="current-password" required value={password} onChange={(event) => setPassword(event.target.value)} /></label>
    {error && <div role="alert" className="error">{error}</div>}
    <button className="primary" type="submit" disabled={loading}>{loading ? "Entrando..." : "Iniciar sesión"}</button>
    <p><Link href="/auth/registro">Registro de usuarios</Link></p>
  </form></main>;
}
