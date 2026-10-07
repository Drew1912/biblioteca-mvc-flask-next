"use client";
import { useRef, useState } from "react";
import { api } from "../model/api";

export function useMutation() {
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const pending = useRef(false);
  async function mutate(path: string, method: string, payload?: unknown, done?: () => void | Promise<void>) {
    if (pending.current) return;
    pending.current = true;
    setBusy(true);
    setError("");
    try {
      await api(path, { method, ...(payload === undefined ? {} : { body: JSON.stringify(payload) }) });
      await done?.();
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "No se pudo completar la operación");
    } finally {
      pending.current = false;
      setBusy(false);
    }
  }
  return { error, busy, mutate };
}
