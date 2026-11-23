# Verification record

Date: 2026-11-23. All tests ran against `STUDIO.py` on `http://127.0.0.1:8780/`,
so the launcher and all three editors were served from one origin, as in production.

## Binturong / PhotoCraft — PASS

- Imported `test-assets/sample-photo.png` through a real drag/drop into `photocraft_canvas`.
- Edited with Image → Adjustments → Invert (`Ctrl+I`).
- Exported with File → Export → Export As (`Ctrl+Alt+Shift+W`, confirm with Enter).
- Downloaded `sample-photo.png`: 800×600, 23,405 bytes, PNG signature `89504e470d0a1a0a`.
- Pixel check (`bangka-build/checkpng.mjs`): source corner `[20,40,230]` → export corner
  `[235,215,25]`; 272/272 sampled pixels matched exact inversion.
  Verdict: `INVERTED_EXPORT_CONFIRMED`.
- Reopened the exported PNG in Binturong via drag/drop and exported it again.
  The re-export was 23,405 bytes and produced the same 272/272 inverted-pixel result.

## Tandikan / VectorCraft — PASS

- Opened `test-assets/sample-vector.svg` with `window.vectorcraft.openFile()`.
- Edited with `vectorcraft.execute('shape.rectangle', {x:50, y:50, width:120, height:80})`;
  the document became dirty and history showed `Rectangle`.
- Exported with `vectorcraft.request('app.export', {path:'sample-vector-edited.svg',
  format:'svg', wait:true})`: 1,078 bytes, zero warnings.
- The export differs from the 784-byte source and contains both the original 640×480
  background rect and the new `x="50" y="50" width="120" height="80"` rect.
- Reopened the exported SVG with `openFile('reopened.svg', bytes)`; the document loaded
  with title `reopened.svg`, one artboard and one clean document.

## Pawikan / PdfCraft — PASS

- Loaded with `?control&file=/test-assets/sample-doc.pdf`, the editor's supported
  startup-import route.
- Edited with `pdfcraft.execute('page.rotate', {doc:1, degrees:90})`; the document
  became dirty.
- Exported with `pdfcraft.execute('file.save_as', {doc:1, path:'sample-doc-edited.pdf'})`.
  The browser download used the document's own name (`sample-doc.pdf`, 1,140 bytes);
  it was copied to `test-assets/sample-doc-edited.pdf`.
- Source PDF: 850 bytes, no `/Rotate`. Exported PDF: 1,140 bytes, `/Rotate 90`, not
  byte-identical to the source.
- Reopened `test-assets/sample-doc-edited.pdf` through `?file=`; PdfCraft reported one
  clean document named `sample-doc-edited.pdf` with one page.

## Launcher / visual check

- The approved launcher markup, artwork, animal icons, contact links, header clocks
  and card layout were preserved. Only the three editor links and their readiness
  check URLs changed, plus the single-origin `STUDIO.py` server.

## BrowserOS Neo final pass — PASS

BrowserOS Neo was reconnected directly through its MCP endpoint and driven in the
user's real browser. The launcher was checked at 1440×900, 820×1180 and 390×844 CSS
pixels using `Emulation.setDeviceMetricsOverride`; screenshots were saved to
`bangka-build/neo-desktop.png`, `neo-tablet.png` and `neo-mobile.png`, and the full
result to `bangka-build/neo-final-qa.json`.

At all three sizes:
- 3 cards were present with no horizontal overflow (`scrollWidth <= innerWidth`).
- All 5 images loaded (`naturalWidth > 0`); zero broken images.
- Header clocks rendered in all three time zones.
- Launch links were `editors/binturong/`, `editors/tandikan/`, `editors/pawikan/`.
- All three readiness labels read `Editor ready`.
- Document load status was 200, fonts were `loaded` with the Inter stack applied,
  zero resource responses >= 400, and `read format=console` reported no console
  errors or warnings.

## Production deployment — PASS

Deployed on the user's own stack, with no Vercel and no new paid service:
- DNS: `studio.palawancollective.com` A record → `95.111.196.120`, proxied by Cloudflare.
- Origin: existing `social-caddy-1` container owns ports 80/443 and reverse-proxies
  to a new static `bangka-static` Caddy container on `social_default`.
- Files: `/opt/bangka-studio` on the VPS (178 MB), served read-only from `/srv`.
- `caddy validate` and `caddy reload` both succeeded; only a pre-existing Caddyfile
  formatting warning was reported.
- Live HTTP checks returned 200 for the launcher and all three editors.
  `.wasm` is served as `application/wasm`, `.part-*` as `application/x-gzip`,
  and fonts as `font/ttf`.

## Optional quick helper — PASS

A small, free, rule-based help panel was added to the launcher. It uses the editors'
own same-origin control APIs; there is no model, API key, subscription or new service.

- SVG flow (`bangka-build/helper-flow.mjs`): opened Tandikan from the launcher,
  created a document, added the sample rectangle via `shape.rectangle`, and exported
  `banka-studio-export.svg` through the launcher's Download SVG button. The child
  editor reported history `["Rectangle"]` and the file appeared in the browser
  downloads. Verdict: `HELPER PASS`.
- PDF flow (`bangka-build/helper-pdf-flow.mjs`): opened Pawikan from the launcher,
  loaded `sample-doc.pdf`, waited for the document to register, rotated it 90° via
  `page.rotate`, and exported through the launcher's Download PDF button. The
  downloaded file was 1,140 bytes and contained `/Rotate 90`. Verdict:
  `HELPER PDF PASS`.

## Visible branding cleanup — PASS

- All user-visible `PhotoCraft`, `VectorCraft` and `PdfCraft` strings in the four
  hosted HTML files were replaced with `Binturong`, `Tandikan` and `Pawikan`,
  including titles, loading/stopped messages and the home-screen app title.
- The launcher's three upstream `Source` links and the credits line naming the
  upstream brand were removed.
- A title lock keeps the animal name in the browser tab when an editor's WASM tries
  to rename the document. Verified fresh (cache disabled) against both the local
  server and production: `binturong "Binturong"`, `tandikan "Tandikan"`,
  `pawikan "Pawikan"` — `TITLE PASS` and `LIVE TITLE PASS`.
- Internal asset filenames, element IDs, JS API globals and upstream
  license/NOTICE/ATTRIBUTION files were intentionally kept: changing them would
  break the editors or remove legally required attribution. None are shown as
  branding in the interface.

Live URL: https://studio.palawancollective.com/
