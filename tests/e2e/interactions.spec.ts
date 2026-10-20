import { test, expect } from "@playwright/test";

test("menú: abre, navega a Nosotros y se cierra", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Abrir menú" }).click();
  const sheet = page.locator("#menu");
  await expect(sheet).toBeVisible();
  await sheet.getByRole("link", { name: "Nosotros" }).click();
  await expect(page).toHaveURL(/\/nosotros\/$/);
  await expect(page.locator("#menu")).toBeHidden();
});

test("formulario de contacto: valida y confirma el envío", async ({ page }) => {
  await page.goto("/contacto/");
  const form = page.locator("form[data-contact]");
  await form.getByRole("button", { name: "Enviar mensaje" }).click();
  await expect(form.locator(".form-status")).toHaveText("Revisa los campos marcados.");
  await expect(form.locator('[name="email"]')).toHaveAttribute("aria-invalid", "true");

  await form.getByLabel("Nombre").fill("Rosa Quispe");
  await form.getByLabel("Correo").fill("rosa@ejemplo.pe");
  await form.getByLabel("Motivo").selectOption("Alianzas");
  await form.getByLabel("Mensaje").fill("Hola, quiero conversar sobre una alianza.");
  await form.locator('[name="consent"]').check();
  await form.getByRole("button", { name: "Enviar mensaje" }).click();
  await expect(page.getByRole("heading", { name: "¡Gracias, Rosa!" })).toBeVisible();
});

test("hero: el chat de ejemplo termina visible con sus 3 ofertas", async ({ page }) => {
  await page.goto("/");
  const offers = page.locator(".screen .offer");
  await expect(offers).toHaveCount(3);
  await page.locator(".screen").scrollIntoViewIfNeeded(); // en pantallas bajas el chat empieza fuera de vista
  await expect(offers.last()).toHaveCSS("opacity", "1", { timeout: 5000 });
});

test.describe("movimiento reducido", () => {
  test.use({ reducedMotion: "reduce" });
  test("las entradas al hacer scroll no desplazan contenido", async ({ page }) => {
    await page.goto("/");
    const card = page.locator("#gratis .card").first();
    await card.scrollIntoViewIfNeeded();
    await expect(card).toHaveCSS("opacity", "1", { timeout: 3000 });
    expect(["none", "0px"]).toContain(await card.evaluate((el) => getComputedStyle(el).translate));
  });
});
