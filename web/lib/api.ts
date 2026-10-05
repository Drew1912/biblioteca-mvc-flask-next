const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:5000/api/v1";

export async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    credentials: "include",
    headers: { "Content-Type": "application/json", ...(options.headers ?? {}) },
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.error ?? "No se pudo completar la operación");
  return data as T;
}

export type User = { id: number; name: string; email: string; role: string; active: boolean };
export type Material = { id: number; type: string; title: string; isbn: string; totalCopies: number; availableCopies: number };
export type Loan = { id: number; material: Material; user: User; dueAt: string; returnedAt: string | null };
