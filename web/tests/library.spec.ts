import { test, expect, Page } from "@playwright/test";
async function login(page: Page, email: string) {
  await page.goto("/login");
  await page.getByLabel("Correo").fill(email);
  await page.getByLabel("Contraseña").fill("Biblioteca123!");
  await page.getByRole("button", { name: "Iniciar sesión" }).click();
  await expect(page.getByRole("heading", { name: "Resumen", exact: true })).toBeVisible();
}
test("login, CRUD, préstamo, devolución y reportes de administrador", async ({ page }, testInfo) => {
  const suffix = Date.now();
  const title = `Lectura E2E ${suffix}`;
  await login(page, "usuario03@test.local");
  await page.screenshot({ path: testInfo.outputPath("admin-panel.png"), fullPage: true });
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
  await page.getByRole("button", { name: "Usuarios", exact: true }).click();
  await page.getByRole("button", { name: "Nuevo usuario" }).click();
  await page.getByLabel("Nombre", { exact: true }).fill(`Persona ${suffix}`);
  await page.getByLabel("Correo", { exact: true }).fill(`e2e-${suffix}@test.local`);
  await page.getByRole("combobox", { name: "Rol", exact: true }).selectOption("bibliotecario");
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
  const createdLoan = page.waitForResponse(response => response.url().endsWith("/loans") && response.request().method() === "POST");
  await page.getByRole("button", { name: "Guardar", exact: true }).click();
  const loan = (await (await createdLoan).json()).loan;
  await expect(page.getByRole("heading", { name: "Registrar préstamo" })).toHaveCount(0);
  await page.locator(`tr[data-loan-id="${loan.id}"]`).getByRole("button", { name: "Devolver", exact: true }).click();
  await expect(page.locator("td .pill").filter({ hasText: /^Devuelto$/ }).first()).toBeVisible();
  await page.getByRole("button", { name: "Reportes", exact: true }).click();
  for (const report of ["inventory", "users", "readers", "loans", "overdue"]) {
    await page.getByRole("combobox", { name: "Reporte", exact: true }).selectOption(report);
    await expect(page.getByRole("table")).toBeVisible();
  }
  await page.getByRole("button", { name: "Cerrar sesión" }).click();
  await expect(page).toHaveURL(/login/);
});
const teacherEmail = process.env.E2E_TEACHER_EMAIL ?? "lector02@test.local";
for (const [email, manage] of [["usuario01@test.local", true], [teacherEmail, false], ["lector01@test.local", false]] as const) {
  test(`acceso y permisos visibles de ${email}`, async ({ page }) => {
    await login(page, email);
    await expect(page.locator(".identity small")).toHaveText(manage ? "bibliotecario" : email === teacherEmail ? "docente" : "estudiante");
    await expect(page.getByRole("button", { name: "Reportes", exact: true })).toHaveCount(manage ? 1 : 0);
    await page.getByRole("button", { name: "Catálogo", exact: true }).click();
    await expect(page.getByRole("table")).toBeVisible();
    await expect(page.getByRole("button", { name: "Nuevo material" })).toHaveCount(manage ? 1 : 0);
    await page.getByLabel("Tipo de material").selectOption("tesis");
    await expect(page.locator("tbody tr").first()).toBeVisible();
    for (const row of await page.locator("tbody tr").all()) await expect(row).toContainText("tesis");
    await page.getByLabel("Solo disponibles").check();
    await expect(page.getByText("Agotado", { exact: true })).toHaveCount(0);
    if (!manage) {
      await page.getByRole("button", { name: "Préstamos", exact: true }).click();
      await expect(page.getByRole("button", { name: "Nuevo préstamo" })).toHaveCount(0);
      await expect(page.getByRole("button", { name: "Devolver", exact: true })).toHaveCount(0);
      const ownName = email === "lector01@test.local" ? "Lector de prueba 01" :
        teacherEmail.startsWith("usuario") ? "Usuario de prueba 02" : "Lector de prueba 02";
      for (const row of await page.locator("tbody tr").all()) await expect(row).toContainText(ownName);
    }
    if (manage) {
      await page.getByRole("button", { name: "Usuarios", exact: true }).click();
      await expect(page.getByRole("button", { name: "Nuevo usuario" })).toHaveCount(0);
      await page.getByRole("button", { name: "Lectores", exact: true }).click();
      await expect(page.getByRole("heading", { name: "Gestión de lectores" })).toBeVisible();
      await expect(page.getByRole("button", { name: "Nuevo lector" })).toHaveCount(0);
    }
  });
}
test("error de login y navegación móvil", async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/login");
  await page.getByLabel("Correo").fill("nadie@test.local");
  await page.getByLabel("Contraseña").fill("invalida");
  await page.getByRole("button", { name: "Iniciar sesión" }).click();
  await expect(page.getByRole("alert").filter({ hasText: "Credenciales inválidas" })).toHaveText("Credenciales inválidas");
  await login(page, "lector01@test.local");
  await page.screenshot({ path: testInfo.outputPath("student-mobile.png"), fullPage: true });
  await page.getByRole("button", { name: "Abrir menú" }).click();
  await page.keyboard.press("Escape");
  await expect(page.getByRole("button", { name: "Abrir menú" })).toBeFocused();
  await page.getByRole("button", { name: "Abrir menú" }).click();
  await page.getByRole("button", { name: "Préstamos", exact: true }).click();
  await expect(page.getByRole("heading", { name: "Mis préstamos", exact: true })).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
});
