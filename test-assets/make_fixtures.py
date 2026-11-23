"""Generate test fixtures for Banka Studio editor checks (stdlib only).

Creates:
  sample-photo.png  -- 800x600 photo-like gradient with shapes (for Binturong)
  sample-vector.svg -- small SVG artwork (for Tandikan)
  sample-doc.pdf    -- one-page PDF with text and vector shapes (for Pawikan)
"""
import struct
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent


def make_png():
    w, h = 800, 600
    rows = []
    for y in range(h):
        row = bytearray()
        row.append(0)  # filter: none
        for x in range(w):
            # sky-to-sunset gradient
            r = 20 + int(200 * (x / w) ** 0.8)
            g = 40 + int(120 * (y / h))
            b = 90 + int(140 * (1 - y / h) ** 1.4)
            # sun disc
            dx, dy = x - 560, y - 210
            if dx * dx + dy * dy < 90 * 90:
                r, g, b = 255, 214, 120
            # "islands" silhouette
            import math
            horizon = 430 + int(38 * math.sin(x / 90.0) + 16 * math.sin(x / 33.0))
            if y > horizon:
                depth = (y - horizon) / (h - horizon)
                r = int(28 + 30 * depth)
                g = int(46 + 34 * depth)
                b = int(44 + 30 * depth)
            row += bytes((min(r, 255), min(g, 255), min(b, 255)))
        rows.append(bytes(row))
    raw = b"".join(rows)

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", ihdr)
           + chunk(b"IDAT", zlib.compress(raw, 9))
           + chunk(b"IEND", b""))
    (HERE / "sample-photo.png").write_bytes(png)
    print("sample-photo.png", len(png), "bytes")


def make_svg():
    svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="640" height="480" viewBox="0 0 640 480">
  <title>Banka Studio vector test card</title>
  <rect width="640" height="480" fill="#10201c"/>
  <circle cx="320" cy="200" r="120" fill="#2e6e5e"/>
  <circle cx="320" cy="200" r="84" fill="#7fc9a6"/>
  <circle cx="320" cy="200" r="48" fill="#e8f6ec"/>
  <path d="M60 420 Q 200 300 340 420 T 620 420" stroke="#c9a86a" stroke-width="14" fill="none" stroke-linecap="round"/>
  <polygon points="320,40 345,110 420,110 360,155 380,225 320,185 260,225 280,155 220,110 295,110"
           fill="#f2c14e"/>
  <text x="320" y="455" font-family="sans-serif" font-size="30" fill="#bcd8c9"
        text-anchor="middle">TANDIKAN VECTOR TEST</text>
</svg>
"""
    (HERE / "sample-vector.svg").write_text(svg, encoding="utf-8")
    print("sample-vector.svg", len(svg), "bytes")


def make_pdf():
    # Minimal but valid one-page PDF with two text runs and a filled rectangle.
    content = b"""BT /F1 28 Tf 72 700 Td (Pawikan PDF Test Page) Tj ET
BT /F1 14 Tf 72 660 Td (Banka Studio - sample document for editing checks.) Tj ET
BT /F1 14 Tf 72 638 Td (Line three: if you can read this after export, text survived.) Tj ET
0.18 0.42 0.36 rg 72 500 200 120 re f 0 0 0 RG 2 w 300 500 220 120 re S"""
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(content)).encode() + b" >>\nstream\n" + content + b"\nendstream",
    ]
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = []
    for i, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode() + body + b"\nendobj\n"
    xref_pos = len(out)
    out += b"xref\n0 " + str(len(objects) + 1).encode() + b"\n"
    out += b"0000000000 65535 f \n"
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += (b"trailer\n<< /Size " + str(len(objects) + 1).encode()
            + b" /Root 1 0 R >>\nstartxref\n" + str(xref_pos).encode() + b"\n%%EOF\n")
    (HERE / "sample-doc.pdf").write_bytes(bytes(out))
    print("sample-doc.pdf", len(out), "bytes")


if __name__ == "__main__":
    make_png()
    make_svg()
    make_pdf()
