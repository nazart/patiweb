# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

`patiweb` is the landing page for **PATI**, a marketplace connecting buyers and
sellers in Gamarra (Lima's garment district) over WhatsApp. It is a **plain
static site**: one `index.html` with inline styles, a small `css/` and `js/`
folder, images and self-hosted fonts. There is no build step, no bundler, no
framework, and no package manager — every file here is served as-is.

The site was originally authored in a design tool and exported as a
bundler-generated `patiweb.html` (base64-inlined assets unpacked to `blob:`
URLs at runtime, plus a proprietary React/Babel/"dc-runtime" client
templating engine). That file is kept in the repo only as a historical
artifact — **it is not the source of truth and should not be edited or
deployed**. The site was later fully unpacked and then rewritten as plain
static HTML (see "Why no client templating engine" below); `index.html` is
the real, current source.

## Structure

```
index.html        # the entire page — plain static HTML, real content in every tag
css/
  fonts.css       # @font-face declarations (Hanken Grotesk, Inter)
  base.css        # reset + header/nav/FAQ-accordion/iOS-mockup component styles
fonts/            # *.woff2 files referenced by css/fonts.css
images/           # *.webp / *.png assets, referenced directly via <img src=...>
                  # (og-image.png is the Open Graph / social-preview image)
js/
  nav-highlight.js # ~20 lines, vanilla JS: highlights the active nav link on
                   # scroll. The only JS the page loads. Everything else
                   # (FAQ accordion, mobile nav) is pure HTML/CSS.
robots.txt         # allows general crawlers + explicitly lists AI crawlers
                   # (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, etc.)
sitemap.xml        # single-URL sitemap
llms.txt           # plain-markdown summary of PATI for LLM agents that don't
                   # render JS/HTML well — keep in sync with the FAQ/steps/
                   # benefits content in index.html if either changes
```

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

No build/install step. Serve the directory with any static file server and
open `index.html`, e.g.:

```
python3 -m http.server 8000
```

There is no test suite or linter in this repo.

## Branches & deploy (AWS Amplify, app `patiweb` / `d3lsvyj4fasecr`)

Git-connected CI/CD: pushing to a tracked branch auto-builds and deploys.

- `main` → production → **https://pati.pe** (custom domain, Route 53 zone
  `pati.pe` in the `pati` AWS profile/account)
- `staging` → **https://dev-web.pati.pe**
- `dev` → local/integration branch, **no Amplify branch, no deploy**

Flow: land changes on `dev` first, merge `dev` → `staging` (verify on
dev-web.pati.pe), then merge `staging` → `main` to ship to production.
