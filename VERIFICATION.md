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

## BrowserOS Neo final pass — PENDING

BrowserOS Neo's MCP tools were not exposed to this OpenCode session during the run
(tool search returned no BrowserOS tools and `http://127.0.0.1:9010/mcp` returned 406).
The user needs to reconnect the agent in the BrowserOS Neo cockpit/MCP connections.
The functional results above came from real headless Chromium sessions driving the
same editor builds, but the requested final desktop/tablet/mobile pass in Neo still
needs to be run after that reconnect.
