import { test, expect } from "@playwright/test";

// Las tiendas exigen URLs públicas de privacidad y de eliminación de cuenta, coherentes con la app.
for (const path of ["/privacidad/", "/terminos/"]) {
  test(`${path}: fecha de vigencia e índice que lleva a cada sección`, async ({ page }) => {
    await page.goto(path);
    await expect(page.locator(".legal-meta time")).toHaveAttribute("datetime", /^\d{4}-\d{2}-\d{2}$/);
    const links = page.locator(".legal-toc a");
    expect(await links.count()).toBeGreaterThan(8);
    for (const href of await links.evaluateAll((as) => as.map((a) => a.getAttribute("href")!))) {
      await expect(page.locator(href), `destino de ${href}`).toHaveCount(1);
    }
    await expect(page.getByText("20616635485").first()).toBeVisible();
  });
}

test("privacidad declara lo que exige la ficha de las tiendas", async ({ page }) => {
  await page.goto("/privacidad/");
  const text = await page.locator("main").innerText();
  for (const must of ["Ley N.º 29733", "ubicación", "EE. UU.", "Twilio", "PostHog", "Gemini", "TypeSafe AI", "Culqi", "logs", "eliminar-cuenta", "18 años", "No vendemos"]) {
    expect(text, must).toContain(must);
  }
  await expect(page.locator('a[href="/eliminar-cuenta/"]').first()).toBeVisible();
});

test("términos: créditos y rol de intermediario", async ({ page }) => {
  await page.goto("/terminos/");
  const text = await page.locator("main").innerText();
  for (const must of ["1 crédito", "20 créditos de bienvenida", "15 créditos gratis", "no cobra ni recibe pagos", "Libro de Reclamaciones"]) {
    expect(text, must).toContain(must);
  }
});

test("eliminar cuenta: pasos en la app, vía alternativa y plazo", async ({ page }) => {
  await page.goto("/eliminar-cuenta/");
  await expect(page.getByRole("heading", { name: "Desde la app" })).toBeVisible();
  await expect(page.getByRole("link", { name: /Pedir por WhatsApp/ })).toHaveAttribute("href", /wa\.me\/51924519233/);
  await expect(page.getByText("30 días").first()).toBeVisible();
});

// Apple 1.2 / Google Play (contenido de usuarios): denunciar, bloquear y plazo de moderación.
test("términos: moderación con denuncia, bloqueo y plazo de 24 horas", async ({ page }) => {
  await page.goto("/terminos/");
  const section = page.locator("#calificaciones");
  await expect(section.getByRole("heading", { name: /denuncias y bloqueo/ })).toBeVisible();
  const text = await section.innerText();
  for (const must of ["Denunciar", "Bloquear", "24 horas", "retirar el contenido", "suspender la cuenta"]) {
    expect(text, must).toContain(must);
  }
  const main = await page.locator("main").innerText();
  expect(main).toContain("no vendemos créditos");
  expect(main).not.toMatch(/puedes comprar (más )?créditos|comprar más dentro de la app/i);
});
