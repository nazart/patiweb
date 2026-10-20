import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { PAGES } from "./pages";

for (const p of PAGES) {
  test(`accesibilidad sin problemas graves en ${p.path}`, async ({ page }) => {
    await page.goto(p.path, { waitUntil: "networkidle" });
    // Espera a que terminen las entradas animadas para medir el contraste final.
    await page.evaluate(() => document.querySelectorAll(".rv").forEach((el) => el.classList.add("in", "done")));
    await page.waitForTimeout(900);
    const results = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa"]).analyze();
    const serious = results.violations.filter((v) => v.impact === "serious" || v.impact === "critical");
    expect(serious.map((v) => `${v.id}: ${v.nodes.map((n) => n.target.join(" ")).slice(0, 3).join(" | ")}`)).toEqual([]);
  });
}
