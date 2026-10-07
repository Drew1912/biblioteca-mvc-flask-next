const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:5000/api/v1";
let csrfToken = "";
export async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
  const writes = options.method && !["GET", "HEAD"].includes(options.method);
  if (writes && !csrfToken) await api("/auth/me");
  const response = await fetch(`${API_URL}${path}`, {
    ...options, credentials: "include", signal: options.signal ?? AbortSignal.timeout(15000),
    headers: { ...(options.body ? { "Content-Type": "application/json" } : {}), ...(writes ? { "X-CSRF-Token": csrfToken } : {}), ...options.headers },
  }).catch((reason: unknown) => {
    const timeout = reason instanceof Error && ["TimeoutError", "AbortError"].includes(reason.name);
    throw new Error(timeout ? "La conexión tardó demasiado. Reintenta la operación." :
      "No se pudo conectar con la biblioteca. Revisa tu conexión e inténtalo de nuevo.");
  });
  const data = await response.json().catch(() => ({}));
  if (data.csrfToken) csrfToken = data.csrfToken;
  if (!response.ok) {
    if (response.status === 401 && path !== "/auth/login") window.location.assign("/login");
    throw new Error(data.error ?? (response.status === 429 ? "Demasiados intentos. Espera un minuto." : "No se pudo completar la operación"));
  }
  if (path === "/auth/logout") csrfToken = "";
  return data as T;
}
export type { User, Material, Loan, Summary } from "./contracts";
