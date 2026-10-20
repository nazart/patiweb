import { test, expect } from "@playwright/test";
import { PAGES, FORBIDDEN } from "./pages";

for (const p of PAGES) {
  test.describe(`página ${p.path}`, () => {
    test(`carga sin errores @smoke`, async ({ page }) => {
      const errors: string[] = [];
      page.on("pageerror", (e) => errors.push(String(e)));
      page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
      const failed: string[] = [];
      page.on("requestfailed", (r) => failed.push(r.url()));
      page.on("response", (r) => { if (r.status() >= 400) failed.push(`${r.status()} ${r.url()}`); });

      const res = await page.goto(p.path, { waitUntil: "networkidle" });
      expect(res?.status()).toBe(200);
      await expect(page.locator("h1")).toHaveCount(1);
      await expect(page.locator("h1")).toContainText(p.h1);
      expect(errors, "errores en consola").toEqual([]);
      expect(failed, "recursos que no cargaron").toEqual([]);
    });

    test("imágenes cargadas, JSON-LD válido y contenido permitido", async ({ page }) => {
      await page.goto(p.path, { waitUntil: "networkidle" });
      // Las imágenes con loading="lazy" pueden no haberse pedido aún: se verifican por HTTP.
      const srcs = await page.$$eval("img", (imgs) => imgs.map((i) => (i as HTMLImageElement).currentSrc || (i as HTMLImageElement).src));
      for (const src of new Set(srcs)) {
        const r = await page.request.get(src);
        expect(r.status(), src).toBe(200);
        expect(r.headers()["content-type"], src).toMatch(/^image\//);
      }

      const ld = await page.locator('script[type="application/ld+json"]').allTextContents();
      expect(ld.length).toBeGreaterThan(0);
      for (const block of ld) expect(() => JSON.parse(block)).not.toThrow();

      const html = await page.content();
      for (const re of FORBIDDEN) expect(html, `texto prohibido ${re}`).not.toMatch(re);
    });
  });
}

test("la página 404 existe", async ({ request }) => {
  const res = await request.get("/404.html");
  expect(res.status()).toBe(200);
  expect(await res.text()).toContain("Esta página no existe, pe.");
});
