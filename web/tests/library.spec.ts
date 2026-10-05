import { test, expect, Page } from "@playwright/test";
async function login(page: Page, email: string) {
  await page.goto("/login");
  await page.getByLabel("Correo").fill(email);
  await page.getByLabel("Contraseña").fill("Biblioteca123!");
  await page.getByRole("button", { name: "Iniciar sesión" }).click();
  await expect(page.getByRole("heading", { name: "Resumen", exact: true })).toBeVisible();
}
test("login, CRUD, préstamo, devolución y reportes de administrador", async ({ page }) => {
  const suffix = Date.now();
  const title = `Lectura E2E ${suffix}`;
  await login(page, "usuario03@test.local");
  await page.getByRole("button", { name: "Catálogo", exact: true }).click();
  await page.getByRole("button", { name: "Nuevo material" }).click();
  await page.getByLabel("Título", { exact: true }).fill(title);
  await page.getByLabel("ISBN / Código").fill(`E2E-${suffix}`);
  await page.getByRole("button", { name: "Guardar", exact: true }).click();
  const row = page.getByRole("row").filter({ hasText: title });
  await expect(row).toBeVisible();
  await row.getByRole("button", { name: "Editar" }).click();
  await page.getByLabel("Título", { exact: true }).fill(`${title} editado`);
  await page.getByRole("button", { name: "Guardar", exact: true }).click();
  await expect(row).toContainText("editado");
  page.on("dialog", dialog => dialog.accept());
  await row.getByRole("button", { name: "Eliminar" }).click();
  await expect(row).toHaveCount(0);
  await page.getByRole("button", { name: "Personas y roles", exact: true }).click();
  await page.getByRole("button", { name: "Nuevo usuario" }).click();
  await page.getByLabel("Nombre", { exact: true }).fill(`Persona ${suffix}`);
  await page.getByLabel("Correo", { exact: true }).fill(`e2e-${suffix}@test.local`);
  await page.getByRole("combobox", { name: "Rol", exact: true }).selectOption("estudiante");
  await page.getByLabel("Contraseña (mínimo 12 caracteres)").fill("Biblioteca123!");
  await page.getByRole("button", { name: "Guardar", exact: true }).click();
  const person = page.getByRole("row").filter({ hasText: `e2e-${suffix}@test.local` });
  await person.getByRole("button", { name: "Editar" }).click();
  await page.getByLabel("Nombre", { exact: true }).fill(`Persona editada ${suffix}`);
  await page.getByRole("button", { name: "Guardar", exact: true }).click();
  await person.getByRole("button", { name: "Eliminar" }).click();
  await expect(person).toHaveCount(0);
  await page.getByRole("button", { name: "Préstamos", exact: true }).click();
  await page.getByRole("button", { name: "Nuevo préstamo" }).click();
  await page.getByRole("combobox", { name: "Material disponible", exact: true }).selectOption({ index: 1 });
  await page.getByRole("combobox", { name: "Persona", exact: true }).selectOption({ index: 1 });
  await page.getByRole("button", { name: "Guardar", exact: true }).click();
  await expect(page.getByRole("heading", { name: "Registrar préstamo" })).toHaveCount(0);
  await page.getByRole("button", { name: "Devolver", exact: true }).last().click();
  await expect(page.locator("td .pill").filter({ hasText: /^Devuelto$/ }).first()).toBeVisible();
  await page.getByRole("button", { name: "Reportes", exact: true }).click();
  for (const report of ["inventory", "users", "loans", "overdue"]) {
    await page.getByRole("combobox", { name: "Reporte", exact: true }).selectOption(report);
    await expect(page.getByRole("table")).toBeVisible();
  }
  await page.getByRole("button", { name: "Cerrar sesión" }).click();
  await expect(page).toHaveURL(/login/);
});
for (const [email, manage] of [["usuario01@test.local", true], ["usuario02@test.local", false], ["lector01@test.local", false]] as const) {
  test(`acceso y permisos visibles de ${email}`, async ({ page }) => {
    await login(page, email);
    await expect(page.getByRole("button", { name: "Reportes", exact: true })).toHaveCount(manage ? 1 : 0);
    await page.getByRole("button", { name: "Catálogo", exact: true }).click();
    await expect(page.getByRole("table")).toBeVisible();
    await expect(page.getByRole("button", { name: "Nuevo material" })).toHaveCount(manage ? 1 : 0);
    if (manage) {
      await page.getByRole("button", { name: "Personas y roles", exact: true }).click();
      await expect(page.getByRole("button", { name: "Nuevo usuario" })).toHaveCount(0);
    }
  });
}
test("error de login y navegación móvil", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/login");
  await page.getByLabel("Correo").fill("nadie@test.local");
  await page.getByLabel("Contraseña").fill("invalida");
  await page.getByRole("button", { name: "Iniciar sesión" }).click();
  await expect(page.getByRole("alert").filter({ hasText: "Credenciales inválidas" })).toHaveText("Credenciales inválidas");
  await login(page, "lector01@test.local");
  await page.getByRole("button", { name: "Préstamos", exact: true }).click();
  await expect(page.getByRole("heading", { name: "Mis préstamos", exact: true })).toBeVisible();
});
