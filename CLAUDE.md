# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This directory contains exactly one file: `patiweb.html`, a self-contained, generated **bundle artifact** (title: "Bundled Page"). There is no source project here — no `package.json`, no build config, no git repo, no README. Do not go looking for a build system, lint config, or test suite; none exists in this directory.

`patiweb.html` is the output of a bundler (consistent with a Pencil/design-tool export) that packages a website into one HTML file for standalone viewing: embedded fonts, images, scripts, and page content are all inlined as base64 data, and a runtime script unpacks them in the browser. The site itself is a React app (React 18.3.1 + ReactDOM, both from unpkg) transpiled in-browser via `@babel/standalone` — there is no separate JS/JSX source tree, the JSX/app code lives only inside the bundle's template string.

**To view it**: open `patiweb.html` directly in a browser. There is nothing to install or build.

## File anatomy

The bundle is one HTML document with a small bootstrap `<script>` followed by four data islands (search for `script type="__bundler/`):

- `__bundler/manifest` — JSON map of `uuid -> { data: base64, compressed: bool, mime? }`. Every embedded asset (fonts, images, JS files, nested-page HTML) is an entry here, keyed by a UUID that also appears as a placeholder (e.g. inside `src="<uuid>"`) in the template.
- `__bundler/ext_resources` — list of `{ id, uuid }`, mapping external resource identifiers (e.g. `https://unpkg.com/react@18.3.1/...`) to the manifest UUID that holds their (locally embedded) contents. `imageSlotsState` is app-specific state, not a script.
- `__bundler/page_order` — UUIDs of nested "pages" (iframe targets), if any. Empty (`[]`) in this file, meaning this bundle has a single page/frame.
- `__bundler/template` — a JSON-encoded HTML string: the actual document (`<html><head>...<body>...`) with manifest UUIDs substituted in as `src`/`url()` placeholders. This is where the real page markup, inline `<style>` (e.g. `@font-face` rules for "Hanken Grotesk"), and app bootstrap script tag live.

At load time the bootstrap script (top of `<head>`, before the data islands) does, in order:
1. Reads the manifest, base64-decodes each entry, gzip-decompresses via `DecompressionStream` if `entry.compressed` is set.
2. Mints a `Blob`/`URL.createObjectURL` for each asset and substitutes the corresponding UUID placeholder in the template with the resulting blob URL.
3. Injects the resulting HTML as the live document.
4. If `page_order` is non-empty, sets up a strict, origin-gated `postMessage` relay so nested page iframes (which ship once, only in the root document's manifest) can request their HTML text from their direct parent — see the large comment block in the bootstrap script for the security reasoning (it guards against a foreign `window.top` — e.g. an artifact host framing this page — spoofing page content).

## Working with this file

- Because the file is a generated artifact, most of it (the manifest and template JSON strings) is effectively opaque binary/minified data on a couple of extremely long lines (checked via `awk '{print length, NR}' patiweb.html | sort -rn`) — do not attempt to hand-edit those lines directly.
- To inspect a specific asset or the real page markup, extract the relevant `script type="__bundler/..."` block (e.g. with `sed -n '<line>p' patiweb.html`) and decode/parse it (`JSON.parse`, then `atob` + optional gunzip for manifest entries) rather than reading the raw line.
- If asked to change the actual site content/behavior, the edit almost always belongs in whatever authored the original `.pen` file or app source that produced this bundle, not in this generated HTML — check with the user before hand-patching the bundle, since regenerating from source is very likely the intended path.
