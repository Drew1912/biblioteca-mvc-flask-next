const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:5000/api/v1";
let csrfToken = "";
export async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
  const writes = options.method && !["GET", "HEAD"].includes(options.method);
  if (writes && !csrfToken) await api("/auth/me");
  const response = await fetch(`${API_URL}${path}`, {
    ...options, credentials: "include",
    headers: { ...(options.body ? { "Content-Type": "application/json" } : {}), ...(writes ? { "X-CSRF-Token": csrfToken } : {}), ...options.headers },
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
export type User = {
  id: number;
  name: string;
  email: string;
  carnetIdentity: string;
  role: string;
  active: boolean;
};
export type Material = { id: number; type: string; title: string; isbn: string; totalCopies: number; availableCopies: number };
export type Loan = { id: number; material: Material; user: User; dueAt: string; returnedAt: string | null };
export type Summary = Record<string, number>;
