export type Role = "administrador" | "bibliotecario" | "docente" | "estudiante";
export type User = {
  id: number;
  name: string;
  email: string;
  carnetIdentity: string;
  role: Role;
  active: boolean;
};
export type Material = {
  id: number; type: "libro" | "revista" | "tesis"; title: string;
  isbn: string; totalCopies: number; availableCopies: number;
};
export type Loan = {
  id: number; material: Material; user: User;
  loanedAt: string; dueAt: string; returnedAt: string | null;
};
export type Summary = Record<string, number>;
export type Section = "overview" | "materials" | "users" | "readers" | "loans" | "reports";
