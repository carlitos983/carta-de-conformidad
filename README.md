# Actas de conformidad – Gráfica Silvestre

Generador web (como [proformas](https://carlitos983.github.io/proformas_grafica/)) para crear **actas de conformidad de servicio** en PDF.

## Uso local

1. Abra `index.html` en Chrome o Edge.
2. Complete cliente, RUC, servicio y la tabla (cantidad + precio).
3. Pulse **Generar PDF del acta**.

La fecha se completa sola (hora Perú).

## Logos

Los mismos de la proforma van en `logos.js`:

```bash
python actualizar-logos.py
```

O use **Importar desde proforma** en la página si falta `logos.js`.

## Publicar en GitHub Pages

1. Cree un repositorio (ej. `actas_conformidad_grafica`).
2. Suba **toda esta carpeta**: `index.html`, `logos.js` (y opcional `actualizar-logos.py`, `LEEME.txt`).
3. En el repo: **Settings → Pages → Branch `main` / carpeta root**.
4. La URL quedará como: `https://TU_USUARIO.github.io/actas_conformidad_grafica/`

> `logos.js` es grande (~250 KB); GitHub lo acepta sin problema.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `index.html` | Formulario + generador PDF |
| `logos.js` | Imágenes del membrete |
| `actualizar-logos.py` | Regenera logos desde el HTML de proformas |
