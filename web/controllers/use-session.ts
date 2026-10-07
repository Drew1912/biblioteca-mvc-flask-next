"use client";
import { useEffect, useState } from "react";
import { api, User } from "../model/api";

export function useSession() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  useEffect(() => {
    let active = true;
    api<{ user: User | null }>("/auth/me")
      .then(data => { if (active) setUser(data.user); })
      .catch(reason => { if (active) setError(reason.message); })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, []);
  return { user, loading, error };
}
