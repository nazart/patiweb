import { test, expect } from "@playwright/test";
import { PAGES, WHATSAPP } from "./pages";

test("enlaces internos existen y WhatsApp apunta al número real", async ({ page, request }) => {
  const internal = new Set<string>();
  for (const p of PAGES) {
    await page.goto(p.path);
    const hrefs = await page.$$eval("a[href]", (as) => as.map((a) => a.getAttribute("href")!));
    for (const h of hrefs) {
      if (h.startsWith("/")) internal.add(h.split("#")[0] || "/");
      if (h.includes("wa.me")) {
        expect(h, `WhatsApp en ${p.path}`).toContain(`wa.me/${WHATSAPP}`);
        expect(decodeURIComponent(h), `código de origen en ${p.path}`).toMatch(/\(#[\w-]+\)/);
      }
    }
  }
  for (const href of internal) {
    const res = await request.get(href);
    expect(res.status(), href).toBe(200);
  }
});
