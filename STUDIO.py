"""Palawan Collective Studio: local-only launcher + upstream WASM app release runner.
Python 3 standard library only; no destructive changes and no external app rebranding.
"""
import functools
import http.server
import json
import mimetypes
import os
from pathlib import Path
import shutil
import socket
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
import webbrowser
import zipfile

ROOT = Path(__file__).resolve().parent
APPS = [('Binturong', 'photocraft', 8765), ('Tandikan', 'vectorcraft', 8766), ('Pawikan', 'pdfcraft', 8768)]
PORT = 8780
mimetypes.add_type('application/wasm', '.wasm')
mimetypes.add_type('application/javascript', '.js')

class StaticHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def log_message(self, fmt, *args):
        if self.path not in ('/favicon.ico',):
            print(' HTTP', self.address_string(), fmt % args)

def get_release(repo):
    req = urllib.request.Request(
        'https://api.github.com/repos/storytold/' + repo + '/releases/latest',
        headers={'User-Agent':'PalawanCollectiveStudioLocal/1.0','Accept':'application/vnd.github+json'})
    with urllib.request.urlopen(req, timeout=35) as resp:
        return json.load(resp)

def zip_asset(release, repo):
    assets = release.get('assets', [])
    matching = [a for a in assets if a.get('name','').lower().endswith('.zip') and
                (repo + '-web-') in a.get('name','').lower()]
    if not matching:
        matching = [a for a in assets if a.get('name','').lower().endswith('.zip') and
                    'web' in a.get('name','').lower()]
    return matching[0] if matching else None

def find_app_dir(root):
    hits = sorted(root.rglob('index.html'), key=lambda p:len(p.parts))
    return hits[0].parent if hits else None

def install(repo):
    dest = ROOT / 'editors' / repo
    ready = find_app_dir(dest) if dest.is_dir() else None
    if ready:
        print('  [READY] Installed web build:', ready)
        return ready
    print('  Looking up official GitHub release for', repo + '...')
    try:
        release = get_release(repo)
        asset = zip_asset(release, repo)
        if not asset:
            print('  [NOT AVAILABLE] Latest official release has no web ZIP:',
                  f'https://github.com/storytold/{repo}/releases/latest')
            return None
        size = asset.get('size', 0)
        print(f"  Downloading {asset['name']} ({size / (1024*1024):.1f} MB)...")
        url = asset['browser_download_url']
        request = urllib.request.Request(url, headers={'User-Agent':'PalawanCollectiveStudioLocal/1.0'})
        (ROOT / 'editors').mkdir(exist_ok=True)
        # Extract to a temporary sibling folder and promote only when a web index exists.
        with tempfile.TemporaryDirectory(prefix='studio-', dir=ROOT / 'editors') as tmp:
            tmpdir = Path(tmp)
            archive = tmpdir / 'download.zip'
            with urllib.request.urlopen(request, timeout=120) as r, open(archive, 'wb') as w:
                shutil.copyfileobj(r,w)
            extract = tmpdir / 'unpacked'
            extract.mkdir()
            with zipfile.ZipFile(archive) as z:
                for entry in z.infolist():
                    dest_path = (extract / entry.filename).resolve()
                    if not dest_path.is_relative_to(extract.resolve()):
                        raise ValueError('Unsafe ZIP member path')
                z.extractall(extract)
            found = find_app_dir(extract)
            if not found:
                raise RuntimeError('Web build ZIP did not contain index.html')
            if dest.exists():
                shutil.rmtree(dest)  # Only the uninitialized editor folder is affected.
            shutil.copytree(found, dest)
        print('  [READY] ', repo, 'web build installed')
        return dest
    except Exception as exc:
        print('  [FAILED] ', type(exc).__name__, str(exc))
        print('  Official downloads:', f'https://github.com/storytold/{repo}/releases/latest')
        return None

def start_server(path, port):
    handler = functools.partial(StaticHandler, directory=str(path))
    try:
        server = http.server.ThreadingHTTPServer(('127.0.0.1', port), handler)
    except OSError as e:
        print(f'  [PORT BUSY] {port}: {e} (an earlier local server may be running)')
        return False
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print(f'  [RUNNING] http://127.0.0.1:{port}/')
    return True

def main():
    print('\nBANKA STUDIO - LOCAL EDITOR STARTER')
    print('Official upstream editor builds; editor interiors are not yet rebranded.\n')
    # Ensure the launcher is accessible first, even if downloads fail.
    start_server(ROOT, PORT)
    webbrowser.open(f'http://127.0.0.1:{PORT}/')
    for label,repo,port in APPS:
        print('\n' + label + ' [' + repo + ']')
        installed = install(repo)
        if installed:
            start_server(installed, port)
    print('\nOpen the Studio and choose Open editor.\n')
    print('Leave this window OPEN while using the editors. Press Ctrl+C to stop.')
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        print('\nStopped.')

if __name__ == '__main__':
    main()
