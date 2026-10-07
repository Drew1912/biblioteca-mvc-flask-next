"use client";
import { useEffect, useState } from "react";
import { api } from "../model/api";

export function useReport(type: string) {
  const [rows, setRows] = useState<unknown[][]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    let active = true;
    setLoading(true);
    setError("");
    api<{ items: unknown[][] }>(`/reports/${type}`)
      .then(data => { if (active) setRows(data.items); })
      .catch(reason => { if (active) setError(reason.message); })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, [type]);
  return { rows, error, loading };
}
