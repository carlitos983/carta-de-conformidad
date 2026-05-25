#!/usr/bin/env python3
"""Extrae imágenes nítidas del PDF de acta (no de proformas) y genera logos.js."""
import base64
import re
from pathlib import Path

try:
    import fitz
except ImportError:
    raise SystemExit("Instale PyMuPDF: pip install pymupdf")

DIR = Path(__file__).resolve().parent
PDF_DEFAULT = Path(r"C:\Users\User\Downloads\ACTA DE CONFORMIDAD GRAFICA SILVESTRE.pdf")
PDF = PDF_DEFAULT if PDF_DEFAULT.is_file() else DIR / "ACTA DE CONFORMIDAD GRAFICA SILVESTRE.pdf"
OUT_JS = DIR / "logos.js"
DPI = 300

# Recortes en puntos PDF (página A4 ~595×842)
HEADER_CLIP = fitz.Rect(0, 0, 595.3, 132)
FOOTER_CLIP = fitz.Rect(0, 718, 595.3, 842)
FIRMA_XREF = 2932  # firma del gerente en el PDF de referencia


def png_to_data_url(path: Path) -> str:
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return "data:image/png;base64," + b64


def main():
    if not PDF.is_file():
        raise SystemExit(f"No se encontró el PDF:\n  {PDF}")

    doc = fitz.open(PDF)
    page = doc[0]
    scale = DPI / 72.0
    mat = fitz.Matrix(scale, scale)

    header_png = DIR / "asset-header.png"
    footer_png = DIR / "asset-footer.png"
    firma_png = DIR / "asset-firma.png"

    page.get_pixmap(matrix=mat, clip=HEADER_CLIP, alpha=False).save(header_png)
    page.get_pixmap(matrix=mat, clip=FOOTER_CLIP, alpha=False).save(footer_png)

    # Firma embebida
    try:
        pix = fitz.Pixmap(doc, FIRMA_XREF)
        if pix.n - pix.alpha > 3:
            pix = fitz.Pixmap(fitz.csRGB, pix)
        pix.save(firma_png)
    except Exception:
        firma_png = None

    doc.close()

    lines = [
        "// Generado por extraer-assets-acta.py — imágenes del PDF de acta (alta resolución)",
        f"// Fuente: {PDF.name} @ {DPI} DPI",
    ]
    lines.append("var IMG_HEADER = '" + png_to_data_url(header_png) + "';")
    lines.append("var IMG_FOOTER = '" + png_to_data_url(footer_png) + "';")
    if firma_png and firma_png.is_file():
        lines.append("var IMG_FIRMA = '" + png_to_data_url(firma_png) + "';")
    else:
        lines.append("var IMG_FIRMA = null;")

    OUT_JS.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("OK:", OUT_JS, "bytes:", OUT_JS.stat().st_size)
    print("  header:", header_png, header_png.stat().st_size)
    print("  footer:", footer_png, footer_png.stat().st_size)
    if firma_png and firma_png.is_file():
        print("  firma:", firma_png, firma_png.stat().st_size)


if __name__ == "__main__":
    main()
