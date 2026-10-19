# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

`patiweb` is the website for **Pati** (pati.pe, read as "pa' ti, pe"), a free
Peruvian app where buyers post what they want and sellers answer with their
price. The site launches the app (Google Play / App Store, 31 Oct 2026) and
invites the community to give feedback; the visual style is "Color peruano"
(yellow #FFD23F, Bricolage Grotesque, sticker cards). Copy never claims
national reach or names cities; Peruvian slang is dosed (hero, closing,
social) while credits/payments/trust/legal copy stays plain. It is a **plain
static site**: a few HTML pages, a small `css/` and `js/` folder, images and
self-hosted fonts. There is no build step, no bundler, no framework, and no
package manager — every file in `web/` is served as-is.

The repo is a small **monorepo**: `web/` (the static site, deployed by
Amplify), `backend/contact/` (the contact-form Lambda), `infra/` (Pulumi IaC
for that backend) and `tools/site/` (the Python generator that writes
`web/`; never deployed).

The site was originally authored in a design tool and exported as a
bundler-generated `patiweb.html` (base64-inlined assets unpacked to `blob:`
URLs at runtime, plus a proprietary React/Babel/"dc-runtime" client
templating engine). That file is kept in the repo only as a historical
artifact (now in `archive/`) — **it is not the source of truth and should
not be edited or deployed**. The site was later fully unpacked and then rewritten as plain
static HTML (see "Why no client templating engine" below); `index.html` is
the real, current source.

## Structure

```
web/                               # the site Amplify publishes (amplify.yml → baseDirectory: web)
  index.html                       # home (8 secciones, ~600 palabras)
  nosotros/ contacto/ novedades/ privacidad/ terminos/ libro-de-reclamaciones/  (index.html each)
  404.html  robots.txt  sitemap.xml  llms.txt
  css/fonts.css css/base.css  fonts/  images/  js/site.js
tools/site/                        # generator (not deployed)
  build.py                         # ALL copy and data live here (FAQ, NEWS, FOUNDERS, LEGAL,
                                   # SOCIALS, store links, CONTACT_MODE/ENDPOINT); writes web/
  base.css pages.css               # concatenated into web/css/base.css
  icons/                           # Simple Icons (CC0) for socials/LinkedIn
backend/contact/                   # Lambda (Node 22 ESM, no dependencies)
  src/handler.mjs                  # MODE=mock (validate + log) | live (DynamoDB → SES + Google Sheets)
  src/validate.mjs src/aws.mjs     # validation; real AWS/Google clients for live
  test/                            # node --test (npm test)
infra/                             # Pulumi (TypeScript), stack "prod", us-east-1
  index.ts                         # DynamoDB, SES domain + DKIM in Route 53, Secrets Manager
                                   # (Google service account), Lambda, HTTP API (CORS, throttling)
.github/workflows/backend.yml      # tests on every change; `pulumi up` on main once enabled
archive/patiweb.html               # historical design-tool export, never deployed
```

**Editing content:** change `tools/site/build.py` (or its CSS), run
`python3 tools/site/build.py`, review `web/`, and commit both. Do not hand-edit
`web/*.html`: the next build overwrites it. Keep `llms.txt` and the FAQ
JSON-LD in sync — the generator does it from the same data.

**Contact form:** `CONTACT_MODE = "simulate"` (current: shows success, sends
nothing). To go live: `pulumi up` in `infra/` with `pati-contact:mode: live`
and `sheetId` set, load the Google service-account JSON into the
`pati-contact/google-sa` secret, then set `CONTACT_MODE = "live"` and
`CONTACT_ENDPOINT` to the `contactEndpoint` output and rebuild.

Company data: Pati.pe, RUC 20616635485, Los Totorales 163, San Miguel.
Email hola@pati.pe (form notifications go to info@pati.pe); WhatsApp
+51 924 519 233; horario L–V 8 a. m.–8 p. m.

## Why no client templating engine

The original export rendered the entire page (H1, steps, FAQ, benefits — all
of it) client-side via React + Babel Standalone + a custom templating runtime
(`{{ binding }}` placeholders, `<sc-for>`/`<sc-if>` loops/conditionals parsed
from a `<x-dc>` template at load time). That meant the raw HTML delivered
over the network contained **no real content** — just literal unrendered
`{{ heroHeadline }}`-style placeholders. Google can render client-side JS (with
caveats), but most AI/LLM crawlers (GPTBot, ClaudeBot, PerplexityBot, CCBot,
etc.) do not execute JavaScript at all, so they saw an effectively empty page.
Since this site is 100% static content with no real interactivity beyond a
FAQ accordion and a mobile nav toggle, the fix was to drop the framework
entirely: every string in `index.html` is real, present-in-the-network-response
text, the FAQ uses native `<details>/<summary>` (works and is crawlable with
zero JS), and the mobile nav hide + sticky header use a CSS media query
(`css/base.css`, `max-width:759px`). This also dropped ~3.9 MB of
React/Babel/runtime JS the browser previously had to fetch and execute just to
transpile JSX for what is, in the end, static markup.

**Consequence for future edits:** because content is now static, any copy
change (steps, benefits, FAQ, hero headline, WhatsApp number) must be edited
directly in `index.html` in every place it repeats, and mirrored in
`llms.txt` and the FAQPage JSON-LD block in `<head>` if it's FAQ content —
there is no single source array driving all of them anymore.

## SEO / GEO notes

- `<head>` carries title, meta description, canonical, Open Graph, Twitter
  Card, and JSON-LD (`Organization` + `WebSite` + `FAQPage`) — all static,
  always present regardless of JS.
- `llms.txt` and `robots.txt` are aimed specifically at LLM/AI crawlers; keep
  `llms.txt` in sync with on-page FAQ/steps/benefits copy.
- Only one `<h1>` on the page (hero headline); section headings are `<h2>`,
  card/step titles are `<h3>`.

## Working locally

```
python3 tools/site/build.py              # regenerate web/
python3 -m http.server 8000 -d web       # preview the site
cd backend/contact && npm test           # backend tests
cd infra && npm install && npm run typecheck
AWS_PROFILE=pati pulumi preview -s prod  # needs a Pulumi backend (pulumi login …)
```

## Branches & deploy (AWS Amplify, app `patiweb` / `d3lsvyj4fasecr`)

Git-connected CI/CD: pushing to a tracked branch auto-builds and deploys.

- `main` → production → **https://pati.pe** (custom domain, Route 53 zone
  `pati.pe` in the `pati` AWS profile/account)
- `staging` → **https://dev-web.pati.pe**
- `dev` → local/integration branch, **no Amplify branch, no deploy**

Flow: land changes on `dev` first, merge `dev` → `staging` (verify on
dev-web.pati.pe), then merge `staging` → `main` to ship to production.

Amplify has a custom rule `/<*>` → `/index.html` (404-200): unknown URLs show
the home with status 200. Consider switching it to `/404.html` (404).

The backend is not deployed yet (contact form simulated). Its workflow only
runs `pulumi up` on `main` when the repo variable `DEPLOY_BACKEND=true` and
`AWS_ROLE_ARN`, `PULUMI_BACKEND_URL` and the secret `PULUMI_CONFIG_PASSPHRASE`
are configured.
