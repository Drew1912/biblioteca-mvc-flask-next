"use client";
import { useState } from "react";
import { useLibrary } from "./use-library";
import { useMutation } from "./use-mutation";
import type { Section } from "../model/contracts";

export function useDashboard() {
  const data = useLibrary();
  const [section, setSection] = useState<Section>("overview");
  const [menuOpen, setMenuOpen] = useState(false);
  const session = useMutation();
  const manage = data.user?.role === "administrador" || data.user?.role === "bibliotecario";
  const labels: Partial<Record<Section, string>> = {
    overview: "Resumen", materials: "Catálogo", loans: "Préstamos",
    ...(manage ? { users: "Usuarios", readers: "Lectores", reports: "Reportes" } : {}),
  };
  function selectSection(id: Section) {
    setSection(id);
    setMenuOpen(false);
  }
  function logout() {
    void session.mutate("/auth/logout", "POST", undefined, () => window.location.assign("/login"));
  }
  return { ...data, section, menuOpen, setMenuOpen, selectSection, logout, manage, labels, session };
}
