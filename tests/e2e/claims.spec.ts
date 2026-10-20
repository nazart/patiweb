import { test, expect, Page } from "@playwright/test";

// Libro de Reclamaciones virtual: campos del Anexo I del reglamento, avisos legales y envío.
async function fill(page: Page, minor = false) {
  const f = page.locator("form[data-claim]");
  await f.getByLabel("Nombres y apellidos").fill("Rosa Quispe Mamani");
  await f.getByLabel("Tipo de documento").selectOption("DNI");
  await f.getByLabel("Número de documento").fill("45678912");
  await f.getByLabel("Domicilio").fill("Av. Universitaria 123, San Miguel");
  await f.getByLabel("Teléfono").fill("+51 999 888 777");
  await f.getByLabel("Correo electrónico").fill("rosa@ejemplo.pe");
  if (minor) {
    await f.getByText("Soy menor de edad").click();
    await f.getByLabel("Nombre del padre, madre o apoderado").fill("Juan Quispe");
    await f.getByLabel("Su documento de identidad").fill("12345678");
  }
  await f.getByLabel("Monto reclamado (S/) (opcional)").fill("25.50");
  await f.getByLabel("Descripción").fill("Uso de la app Pati");
  await f.getByLabel("Detalle").fill("La oferta que acepté cambió de precio al llegar a la tienda.");
  await f.getByLabel("Pedido").fill("Que revisen al vendedor.");
  await f.locator('[name="accept"]').check();
  return f;
}

test("muestra los datos del proveedor, las definiciones y los avisos legales", async ({ page }) => {
  await page.goto("/libro-de-reclamaciones/");
  const main = page.locator("main");
  for (const must of ["Pati.pe", "20616635485", "Los Totorales 163", "Reclamo:", "Queja:", "15) días hábiles", "Indecopi"]) {
    await expect(main).toContainText(must);
  }
  await expect(page.locator("[data-today]")).not.toHaveText("hoy");
});

test("valida los campos obligatorios y el documento según su tipo", async ({ page }) => {
  await page.goto("/libro-de-reclamaciones/");
  const f = page.locator("form[data-claim]");
  await f.getByRole("button", { name: "Enviar hoja de reclamación" }).click();
  await expect(f.locator(".form-status")).toHaveText("Revisa los campos marcados.");
  await f.getByLabel("Número de documento").fill("123");
  await f.getByRole("button", { name: "Enviar hoja de reclamación" }).click();
  await expect(f.locator('[name="docNumber"]')).toHaveAttribute("aria-invalid", "true");
});

test("menor de edad: pide los datos del padre, madre o apoderado", async ({ page }) => {
  await page.goto("/libro-de-reclamaciones/");
  const guardian = page.getByLabel("Nombre del padre, madre o apoderado");
  await expect(guardian).toBeHidden();
  await page.getByText("Soy menor de edad").click();
  await expect(guardian).toBeVisible();
});

test("modo correo: genera la hoja con código y la envía por correo o WhatsApp", async ({ page }) => {
  await page.goto("/libro-de-reclamaciones/");
  const f = await fill(page, true);
  await f.getByRole("button", { name: "Enviar hoja de reclamación" }).click();
  const result = page.locator(".claim-result");
  await expect(result).toBeVisible();
  await expect(result.locator("[data-number]")).toHaveText(/^LR-\d{8}-\d{6}$/);
  const copy = await result.locator(".claim-copy").innerText();
  for (const must of ["RUC 20616635485", "DNI: 45678912", "Juan Quispe", "S/ 25.50", "Pedido: Que revisen al vendedor.", "15 días hábiles"]) expect(copy).toContain(must);
  const mail = await result.locator('[data-send="email"]').getAttribute("href");
  expect(mail).toMatch(/^mailto:hola@pati\.pe\?subject=/);
  expect(decodeURIComponent(mail!)).toContain("DNI: 45678912");
  await expect(result.locator('[data-send="whatsapp"]')).toHaveAttribute("href", /wa\.me\/51924519233/);
});

test("modo backend: registra la hoja y muestra el número correlativo", async ({ page }) => {
  await page.route("**/api-test/reclamos", (route) =>
    route.fulfill({ json: { ok: true, number: "LR-2026-000007", createdAt: "2026-11-03T15:00:00.000Z", emailed: true } }));
  await page.goto("/libro-de-reclamaciones/");
  await page.locator("form[data-claim]").evaluate((f) => { f.setAttribute("data-mode", "live"); f.setAttribute("data-endpoint", "/api-test/reclamos"); });
  const f = await fill(page);
  const req = page.waitForRequest("**/api-test/reclamos");
  await f.getByRole("button", { name: "Enviar hoja de reclamación" }).click();
  const body = (await req).postDataJSON();
  expect(body).toMatchObject({ docType: "DNI", docNumber: "45678912", claimType: "reclamo", itemType: "servicio", accept: true });
  await expect(page.locator(".claim-result [data-number]")).toHaveText("LR-2026-000007");
  await expect(page.locator(".claim-next")).toContainText("Te enviamos una copia a rosa@ejemplo.pe");
});
