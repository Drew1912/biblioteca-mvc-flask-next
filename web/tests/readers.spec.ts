import { test, expect } from "@playwright/test";

test("administrador gestiona docentes y estudiantes con reportes separados", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel("Correo").fill("usuario03@test.local");
  await page.getByLabel("Contraseña").fill("Biblioteca123!");
  await page.getByRole("button", { name: "Iniciar sesión" }).click();
  await page.getByRole("button", { name: "Lectores", exact: true }).click();
  for (const role of ["docente", "estudiante"]) {
    const email = `${role}-${Date.now()}@test.local`;
    await page.getByRole("button", { name: "Nuevo lector", exact: true }).click();
    await page.getByLabel("Nombre", { exact: true }).fill(`Lector ${role}`);
    await page.getByLabel("Correo", { exact: true }).fill(email);
    await page.getByLabel("Carnet de identidad").fill(`CI-${Date.now()}`);
    const roles = page.getByRole("combobox", { name: "Rol", exact: true });
    await expect(roles.locator("option")).toHaveText(["Seleccionar…", "estudiante", "docente"]);
    await roles.selectOption(role);
    await page.getByLabel("Contraseña (mínimo 12 caracteres)").fill("Biblioteca123!");
    await page.getByRole("button", { name: "Guardar", exact: true }).click();
    const row = page.getByRole("row").filter({ hasText: email });
    await expect(row).toContainText(role);
    await row.getByRole("button", { name: "Editar", exact: true }).click();
    await page.getByLabel("Nombre", { exact: true }).fill(`Lectura ${role}`);
    await page.getByRole("button", { name: "Guardar", exact: true }).click();
    await expect(row).toContainText(`Lectura ${role}`);
    await page.getByRole("button", { name: "Reportes", exact: true }).click();
    await page.getByRole("combobox", { name: "Reporte", exact: true }).selectOption("readers");
    await expect(page.getByRole("row").filter({ hasText: email })).toBeVisible();
    await page.getByRole("combobox", { name: "Reporte", exact: true }).selectOption("users");
    await expect(page.getByRole("row").filter({ hasText: email })).toHaveCount(0);
    await page.getByRole("button", { name: "Lectores", exact: true }).click();
    page.once("dialog", dialog => dialog.accept());
    await row.getByRole("button", { name: "Eliminar", exact: true }).click();
    await expect(row).toHaveCount(0);
  }
});

test("un error de conexión es visible y permite reintentar", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel("Correo").fill("lector01@test.local");
  await page.getByLabel("Contraseña").fill("Biblioteca123!");
  await page.getByRole("button", { name: "Iniciar sesión" }).click();
  await expect(page.getByRole("heading", { name: "Resumen", exact: true })).toBeVisible();
  await page.route("**/api/v1/materials", route => route.abort());
  await page.reload();
  await expect(page.locator("main [role=alert]")).toBeVisible();
  await expect(page.getByRole("status")).toHaveCount(0);
  await page.unroute("**/api/v1/materials");
  await page.getByRole("button", { name: "Reintentar", exact: true }).click();
  await expect(page.locator("main [role=alert]")).toHaveCount(0);
  await page.getByRole("button", { name: "Catálogo", exact: true }).click();
  await expect(page.locator("tbody tr").first()).toBeVisible();
});
