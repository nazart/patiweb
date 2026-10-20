import { defineConfig, devices } from "@playwright/test";

// Por defecto prueba la web local (web/ servida en :4173).
// BASE_URL=https://dev-web.pati.pe npm run test:smoke  → prueba un sitio desplegado.
const baseURL = process.env.BASE_URL || "http://localhost:4173";
const local = !process.env.BASE_URL;

export default defineConfig({
  testDir: "tests/e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? [["list"], ["html", { open: "never" }]] : "list",
  use: { baseURL, trace: "retain-on-failure" },
  projects: [
    { name: "iphone", use: { ...devices["iPhone 13"] } },
    { name: "android", use: { ...devices["Pixel 7"] } },
  ],
  webServer: local
    ? { command: "python3 -m http.server 4173 --directory web", url: "http://localhost:4173", reuseExistingServer: !process.env.CI, stdout: "ignore", stderr: "ignore" }
    : undefined,
});
