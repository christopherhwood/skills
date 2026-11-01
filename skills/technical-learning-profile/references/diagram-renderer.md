# Diagram renderer

Requires Node.js 22.13+ and npm. Paths below are relative to this skill directory. Install the pinned dependency once:

```sh
npm ci
```

This downloads Mermaid CLI and its Puppeteer browser. For an existing Chrome installation, set `PUPPETEER_SKIP_DOWNLOAD=true` during installation, then pass its executable path when rendering.

```sh
node scripts/render-diagram.mjs /path/to/diagram.mmd --output /path/to/diagram.png
node scripts/render-diagram.mjs /path/to/diagram.mmd --output /path/to/diagram.svg --size 1400
node scripts/render-diagram.mjs /path/to/diagram.mmd --output /path/to/diagram.png --browser '/path/to/chrome'
```

PNG is the default presentation format; SVG and PDF are also supported. Options: `--size` (400–4000, maximum dimension in CSS pixels, default 1200), `--scale` (1–4, default 2), `--browser`, and `--force` to replace an existing output. Source and output must differ. The renderer uses a white background, consistent typography, and Mermaid's base theme. Diagram-level styling remains possible.

The command prints JSON containing the absolute output path, byte size, and format. Errors return a nonzero exit code with diagnostics. Failed rendering does not replace an existing output. Files are staged beside the output and cleaned up afterward. No shell interpolation or automatic package installation occurs during rendering.

Inspect the actual PNG (or a raster preview of SVG/PDF) before presenting it. Check labels, overlaps, arrow direction, physical versus logical boundaries, and whether the drawing preserves the mechanism. Rendering is not a layout-quality or correctness certification. Keep source and generated diagrams in the task workspace, not the installed skill. Render diagrams you authored or reviewed; this wrapper is not a sandbox for untrusted browser content.
