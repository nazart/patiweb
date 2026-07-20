# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

`patiweb` is the landing page for **PATI**, a marketplace connecting buyers and
sellers in Gamarra (Lima's garment district) over WhatsApp. It's a static
site: plain HTML + CSS + images + fonts, plus a small React app that renders
one custom component (an iOS phone-frame mockup in the hero) via an
in-browser Babel transpile. There is no build step and no package manager —
everything is served as-is.

The site was originally authored in a design tool and exported as a single
1.6 MB self-contained bundle (`patiweb.html`, kept in the repo for reference/
history). That file is a "bundler" build artifact: fonts, images and JS were
all inlined as base64 inside `<script type="__bundler/...">` blocks and
unpacked into `blob:` URLs at load time. It has since been unpacked into the
real static structure described below — **`patiweb.html` is not the source
of truth and should not be edited**; treat `index.html` + the asset folders
as the actual project.

## Structure

```
index.html        # the page — plain static HTML, no build step
css/
  fonts.css       # @font-face declarations (Hanken Grotesk, Inter)
  base.css        # reset/base rules (body, *, a, button, ::selection)
fonts/            # *.woff2 files referenced by css/fonts.css
images/           # *.webp / *.png assets used directly via src=
js/
  dc-runtime.js   # GENERATED — page-templating/component runtime. Do not
                  # hand-edit; upstream source is `dc-runtime/src/*.ts`,
                  # rebuilt with `bun run build` (that source isn't in this
                  # repo). It parses the `<x-dc>`/`<helmet>`/`{{ }}` markup
                  # in index.html and resolves `<x-import>` tags.
  image-slot.js   # defines the `<image-slot>` custom element used for every
                  # photo/screenshot placeholder on the page
  ios-frame.jsx   # the `IOSDevice` phone-frame mockup shown in the hero
                  # (React, transpiled in-browser by Babel Standalone)
  vendor/         # react, react-dom, babel-standalone — vendored locally
                  # (not loaded from unpkg) so the site has no runtime CDN
                  # dependency
```

## How the page is wired together

`index.html`'s `<head>` sets `window.__resources` — a map from an id/URL to a
local override path — **before** loading `js/dc-runtime.js`. Today it only
overrides the three vendor library URLs (so `dc-runtime`'s internal
`fetch()`/`<x-import>` resolution finds the local copies in `js/vendor/`
instead of unpkg):

```html
<script>
window.__resources = {
  "https://unpkg.com/react@18.3.1/umd/react.production.min.js": "js/vendor/react.production.min.js",
  ...
};
</script>
<script src="js/dc-runtime.js"></script>
```

The body is a `dc-runtime` document: an `<x-dc>` root containing a
`<helmet data-dc-atomics="">` (link/style tags `dc-runtime` hoists into the
real `<head>` at runtime), the page markup with `{{ binding }}` placeholders,
and a `<script type="text/x-dc" data-dc-script data-props="...">` holding the
page's editable props (`heroVariant`, `whatsappNumber`) and small bits of JS
(e.g. the `steps` array for the "how it works" section).

Images use `<x-import component-from-global-scope="image-slot" from="js/image-slot.js" id="..." src="images/...">`.
**`src=` is the only path that reliably shows a real file**: `image-slot.js`
also supports a design-tool-only "sidecar" state file
(`window.__resources.imageSlotsState`), but it deliberately only trusts a
`data:image/...` URI from that sidecar — a plain file path there is silently
ignored (see the comment above `_render()` in `image-slot.js`). This repo
doesn't use the sidecar at all; every image is wired via a literal `src=`
attribute (or `src="{{ step.imgSrc }}"` for the templated step screenshots),
which the component always honors. One consequence: any pan/zoom "reframe"
(the `x`/`y`/`s` crop the design tool stores per image) only applies through
the sidecar path, so images placed via `src=` always render with the default
centered `object-fit: cover` framing.

## Working locally

No build/install step. Serve the directory with any static file server and
open `index.html`, e.g.:

```
python3 -m http.server 8000
```

There is no test suite or linter in this repo.
