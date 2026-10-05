"use client";
import { useCallback, useEffect, useState } from "react";
import { api, Loan, Material, Summary, User } from "../model/api";
export function useLibrary() {
  const [user, setUser] = useState<User | null>(null);
  const [materials, setMaterials] = useState<Material[]>([]);
  const [loans, setLoans] = useState<Loan[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [summary, setSummary] = useState<Summary>({});
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const load = useCallback(async () => {
    setError("");
    try {
      const me = await api<{ user: User | null }>("/auth/me");
      if (!me.user) { window.location.assign("/login"); return; }
      const manage = ["administrador", "bibliotecario"].includes(me.user.role);
      const [catalog, history, people, stats] = await Promise.all([
        api<{ items: Material[] }>("/materials"), api<{ items: Loan[] }>("/loans"),
        manage ? api<{ items: User[] }>("/users") : Promise.resolve({ items: [] }),
        manage ? api<Summary>("/reports/summary") : Promise.resolve({}),
      ]);
      setUser(me.user); setMaterials(catalog.items); setLoans(history.items);
      setUsers(people.items); setSummary(stats);
    } catch (reason) { setError(reason instanceof Error ? reason.message : "Error de conexión"); }
    finally { setLoading(false); }
  }, []);
  useEffect(() => { void load(); }, [load]);
  return { user, materials, loans, users, summary, error, loading, load };
}
