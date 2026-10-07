import { test, expect } from "@playwright/test";

test("registro tiene ruta y orientación para visitantes", async ({ page }) => {
  const response = await page.goto("/auth/registro");
  expect(response?.status()).toBe(200);
  await expect(page.getByRole("heading", { name: "Registro de usuarios" })).toBeVisible();
  await expect(page.getByText("El registro de cuentas lo realiza", { exact: false })).toBeVisible();
  await expect(page.getByRole("button", { name: "Guardar", exact: true })).toHaveCount(0);
  await page.getByRole("link", { name: "Iniciar sesión" }).click();
  await expect(page).toHaveURL(/\/login$/);
  await page.getByRole("link", { name: "Registro de usuarios" }).click();
  await expect(page).toHaveURL(/\/auth\/registro$/);
});

test("administrador registra desde la URL y conserva su sesión", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel("Correo").fill("usuario03@test.local");
  await page.getByLabel("Contraseña").fill("Biblioteca123!");
  await page.getByRole("button", { name: "Iniciar sesión" }).click();
  await expect(page.getByRole("heading", { name: "Resumen", exact: true })).toBeVisible();
  await page.goto("/auth/registro");
  const email = `registro-${Date.now()}@test.local`;
  await page.getByLabel("Nombre", { exact: true }).fill("Registro de prueba");
  await page.getByLabel("Correo", { exact: true }).fill(email);
  const roles = page.getByRole("combobox", { name: "Rol", exact: true });
  await expect(roles.locator("option")).toHaveText(["Seleccionar…", "estudiante", "docente", "bibliotecario", "administrador"]);
  await roles.selectOption("estudiante");
  await page.getByLabel("Contraseña (mínimo 12 caracteres)").fill("Biblioteca123!");
  await page.getByRole("button", { name: "Guardar", exact: true }).click();
  await expect(page.getByRole("status")).toHaveText("Usuario registrado correctamente.");
  await page.getByRole("link", { name: "Volver al panel" }).click();
  await page.getByRole("button", { name: "Lectores", exact: true }).click();
  const row = page.getByRole("row").filter({ hasText: email });
  await expect(row).toBeVisible();
  page.on("dialog", dialog => dialog.accept());
  await row.getByRole("button", { name: "Eliminar" }).click();
  await expect(row).toHaveCount(0);
});

test("un lector no recibe el formulario de alta", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel("Correo").fill("lector01@test.local");
  await page.getByLabel("Contraseña").fill("Biblioteca123!");
  await page.getByRole("button", { name: "Iniciar sesión" }).click();
  await expect(page.getByRole("heading", { name: "Resumen", exact: true })).toBeVisible();
  await page.goto("/auth/registro");
  await expect(page.getByText("El registro de cuentas lo realiza", { exact: false })).toBeVisible();
  await expect(page.getByRole("button", { name: "Guardar", exact: true })).toHaveCount(0);
});
