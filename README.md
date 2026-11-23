# Banka Studio

A Palawan Collective creative studio built around open-source Rust / WebAssembly editors.

## Creative tools

| Banka Studio name | Upstream engine | Purpose |
|---|---|---|
| Binturong | [PhotoCraft](https://github.com/storytold/photocraft) | Image editing |
| Tandikan | [VectorCraft](https://github.com/storytold/vectorcraft) | Vector design |
| Pawikan | [PdfCraft](https://github.com/storytold/pdfcraft) | PDF editing |

## Test the actual editors on Windows

1. Install Python 3 if not installed.
2. Clone this repository or download its contents, then double-click `START-STUDIO.bat`.
3. Visit `http://127.0.0.1:8780` and select **Open editor**. Leave the terminal open.

The launcher starts locally and attempts to fetch official upstream WebAssembly editor releases. The upstream editor builds are downloaded on your own machine under `editors/`; the launcher does **not** contain those editor engines. If unavailable, the starter reports the failure and you may use official native installers instead.

### Website hosting

The root `index.html` and `assets/` are a static launcher preview. **Its `127.0.0.1` editor links do not work from a remote domain** until each browser editor has been installed and served at a valid public URL. Do not treat the launcher alone as a functional hosted suite.

### Licensing

Upstream code is MIT or Apache-2.0 (check each project), while upstream trademarks and brand art may have separate restrictions. Preserve required notices and do not represent the original editor interfaces as already rebranded.
