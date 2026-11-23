"""Banka Studio local launcher: serves the studio and the three editors from one origin.

Python 3 standard library only. The editors under ``editors/`` are the official
upstream WebAssembly builds (PhotoCraft, VectorCraft, PdfCraft — see NOTICE.md);
they run entirely in the browser, so a plain static file server is all that is
needed locally. The same folder layout is what gets deployed, so what you test
here behaves exactly like the hosted site.
"""
import functools
import http.server
import mimetypes
import socket
import sys
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PORT = 8780
EDITORS = [
    ('Binturong', 'binturong', 'photocraft'),
    ('Tandikan', 'tandikan', 'vectorcraft'),
    ('Pawikan', 'pawikan', 'pdfcraft'),
]

mimetypes.add_type('application/wasm', '.wasm')
mimetypes.add_type('text/javascript', '.js')
mimetypes.add_type('font/ttf', '.ttf')
mimetypes.add_type('font/otf', '.otf')


class StaticHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        # Revalidate the shell; hashed editor assets get long cache via deploy config.
        if self.path in ('/', '/index.html'):
            self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def log_message(self, fmt, *args):
        if self.path != '/favicon.ico':
            print(' HTTP', self.address_string(), fmt % args)


def check_editors():
    ok = True
    for label, folder, upstream in EDITORS:
        index = ROOT / 'editors' / folder / 'index.html'
        if index.is_file():
            print(f'  [READY] {label:9s} -> /editors/{folder}/  (upstream: {upstream})')
        else:
            ok = False
            print(f'  [MISSING] {label}: editors/{folder}/index.html not found. '
                  'Re-pull this repository (the editor builds are committed).')
    return ok


def start_server():
    try:
        server = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), StaticHandler)
    except OSError as exc:
        print(f'  [PORT BUSY] {PORT}: {exc} (an earlier studio server may be running)')
        return False
    threading = __import__('threading')
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print(f'  [RUNNING] http://127.0.0.1:{PORT}/')
    return True


def main():
    print('\nBANKA STUDIO - LOCAL EDITOR SERVER')
    print('One origin serves the launcher and all three editors.\n')
    check_editors()
    start_server()
    url = f'http://127.0.0.1:{PORT}/'
    print(f'\nOpening {url} ...')
    webbrowser.open(url)
    print('Leave this window OPEN while using the editors. Press Ctrl+C to stop.')
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        print('\nStopped.')


if __name__ == '__main__':
    main()
