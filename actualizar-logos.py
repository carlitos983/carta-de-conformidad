#!/usr/bin/env python3
"""Genera logos.js desde el HTML de proformas (mismos logos en el PDF)."""
import re
from pathlib import Path

CANDIDATOS = [
    Path(__file__).resolve().parent / "proforma-ref.html",
    Path(r"C:\Users\User\Downloads\index anterior a actualizacion de imagenes.html"),
    Path(__file__).resolve().parent.parent / "proformas" / "index.html",
    Path.home() / "proformas_grafica" / "index.html",
]

OUT = Path(__file__).resolve().parent / "logos.js"

src = None
for p in CANDIDATOS:
    if p.is_file():
        src = p
        break

if not src:
    raise SystemExit(
        "No se encontró el HTML de proformas.\n"
        "Copie su generador de proformas como:\n"
        "  carta de conformidad/proforma-ref.html\n"
        "o deje el archivo en Descargas con el nombre habitual."
    )

text = src.read_text(encoding="utf-8")
out_lines = ["// Generado por actualizar-logos.py — no editar a mano", f"// Fuente: {src.name}"]
for name in ("IMG_LOGO", "IMG_FOTO"):
    m = re.search(r"var " + name + r"='([^']+)'", text)
    if not m:
        raise SystemExit(f"No se encontró {name} en {src}")
    out_lines.append(f"var {name} = '{m.group(1)}';")

OUT.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
print("OK:", OUT, "bytes:", OUT.stat().st_size)
