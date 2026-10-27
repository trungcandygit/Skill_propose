#!/usr/bin/env python3
"""Check figure files for print size, resolution, font embedding and effective font size.

Why: a figure designed at 10 in wide and printed at 6.5 in shrinks every font
by 35%; 9 pt labels become 5.9 pt, below the journal minimum (tables-figures
card TF-37, TF-48 to TF-51). The arithmetic is simple but easy to forget, and
font embedding can only be seen with a tool. This script does both.

Inputs (any mix)
  image files (.png .jpg .jpeg .tif .tiff)   pixel size, dpi metadata (Pillow if
                                             installed, else PNG header only)
  PDF files                                  page size (pdfinfo), fonts and
                                             whether each is embedded (pdffonts)
  --docx paper.docx                          every embedded image with the width
                                             it is displayed at in the document

Effective font size = design font size × (print width / design width).
  design width: --design-width inches, else pixels / dpi metadata, else PDF
                page width.
  print width : --print-width inches, else the displayed width in the docx,
                else 6.5 in (full text width) as a stated assumption.
  design font : --font-pt (the base_size you used, default 9 pt) for every
                file; the result says how big that font prints.
A warning is raised when the effective size is below --min-pt (default 9; use
the journal's rule, e.g. 7 for Elsevier, 5 for Nature) or the effective
resolution at print size is below --min-dpi (default 300).

Usage
  python3 check_figure.py fig1.png fig2.pdf [--print-width 6.5] [--font-pt 9]
  python3 check_figure.py --docx paper.docx [--font-pt 10] [--out report.md]

Standard library plus optional Pillow and poppler (pdfinfo, pdffonts); a
check that needs a missing tool is reported as UNVERIFIED, not skipped.
"""
import argparse
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import zipfile

try:
    from PIL import Image  # optional
except ImportError:  # pragma: no cover
    Image = None

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def png_header(path):
    with open(path, "rb") as fh:
        data = fh.read(4096)
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h = struct.unpack(">II", data[16:24])
    dpi = None
    i = data.find(b"pHYs")
    if i > 0:
        x, y, unit = struct.unpack(">IIB", data[i + 4:i + 13])
        if unit == 1:
            dpi = (x * 0.0254, y * 0.0254)
    return w, h, dpi


def image_info(path):
    if Image is not None:
        try:
            with Image.open(path) as im:
                dpi = im.info.get("dpi")
                return im.size[0], im.size[1], (float(dpi[0]), float(dpi[1])) if dpi else None, im.mode
        except Exception as e:  # noqa: BLE001
            return None, None, None, f"unreadable: {e}"
    ph = png_header(path)
    if ph:
        return ph[0], ph[1], ph[2], "?"
    return None, None, None, "UNVERIFIED: Pillow not installed and not a PNG"


def pdf_info(path):
    out = {"pages": None, "width_in": None, "fonts": [], "notes": []}
    if shutil.which("pdfinfo"):
        r = subprocess.run(["pdfinfo", path], capture_output=True, text=True)
        m = re.search(r"Page size:\s+([\d.]+) x ([\d.]+) pts", r.stdout)
        if m:
            out["width_in"] = float(m.group(1)) / 72.0
            out["height_in"] = float(m.group(2)) / 72.0
        m = re.search(r"Pages:\s+(\d+)", r.stdout)
        out["pages"] = int(m.group(1)) if m else None
    else:
        out["notes"].append("UNVERIFIED: pdfinfo not found (page size unknown)")
    if shutil.which("pdffonts"):
        r = subprocess.run(["pdffonts", path], capture_output=True, text=True)
        for line in r.stdout.splitlines()[2:]:
            parts = line.split()
            if len(parts) >= 7:
                # columns: name type [encoding...] emb sub uni object ID
                emb, sub = parts[-5], parts[-4]
                out["fonts"].append((parts[0], " ".join(parts[1:-5]), emb, sub))
    else:
        out["notes"].append("UNVERIFIED: pdffonts not found (embedding unknown)")
    return out


def judge(eff_pt, eff_dpi, args):
    w = []
    if eff_pt is not None and eff_pt < args.min_pt - 0.05:
        w.append(f"FONT: {args.font_pt:g} pt at design size prints at {eff_pt:.1f} pt (< {args.min_pt:g} pt)")
    if eff_dpi is not None and eff_dpi < args.min_dpi - 0.5:
        w.append(f"RESOLUTION: {eff_dpi:.0f} dpi at print size (< {args.min_dpi:g})")
    return w


def report_image(path, label, print_w, args, lines):
    w, h, dpi, mode = image_info(path)
    if w is None:
        lines.append(f"- {label}: {mode}")
        return 1
    design_w = args.design_width or (w / dpi[0] if dpi and dpi[0] > 1 else None)
    pw = print_w or args.print_width
    assumed = "" if (print_w or args.print_width_given) else " (assumed text width)"
    eff_dpi = w / pw if pw else None
    eff_pt = args.font_pt * pw / design_w if design_w and pw else None
    lines.append(f"- {label}: {w}x{h} px, mode {mode}, dpi metadata {('%.0f' % dpi[0]) if dpi else 'none'}, "
                 f"design width {('%.2f in' % design_w) if design_w else 'unknown'}, print width {pw:.2f} in{assumed}, "
                 f"effective {eff_dpi:.0f} dpi" + (f", {args.font_pt:g} pt prints at {eff_pt:.1f} pt" if eff_pt else ", effective font size UNVERIFIED (no design width; pass --design-width)"))
    if mode in ("RGBA", "LA", "P") and path.lower().endswith((".tif", ".tiff")):
        lines.append("  - TIFF with alpha or palette: some journals (PLOS) reject alpha channels")
    if path.lower().endswith((".png", ".jpg", ".jpeg")):
        lines.append("  - raster file: a chart or line plot should also exist as vector PDF/EPS for production (TF-48)")
    warns = judge(eff_pt, eff_dpi, args)
    for x in warns:
        lines.append(f"  - WARN {x}")
    return len(warns)


def report_pdf(path, print_w, args, lines):
    info = pdf_info(path)
    design_w = args.design_width or info.get("width_in")
    pw = print_w or args.print_width
    eff_pt = args.font_pt * pw / design_w if design_w and pw else None
    unemb = [f for f in info["fonts"] if f[2] != "yes"]
    t3 = [f for f in info["fonts"] if "Type 3" in f[1]]
    lines.append(f"- {os.path.basename(path)}: {info['pages']} page(s), page width {('%.2f in' % design_w) if design_w else 'unknown'}, "
                 f"print width {pw:.2f} in, {len(info['fonts'])} fonts, {len(unemb)} not embedded"
                 + (f", {args.font_pt:g} pt prints at {eff_pt:.1f} pt" if eff_pt else ""))
    for n in info["notes"]:
        lines.append(f"  - {n}")
    for f in unemb:
        lines.append(f"  - WARN font not embedded: {f[0]} ({f[1]})")
    for f in t3:
        lines.append(f"  - WARN Type 3 font {f[0]}: use cairo_pdf (R) or pdf.fonttype = 42 (matplotlib)")
    if not info["fonts"] and shutil.which("pdffonts"):
        lines.append("  - no fonts: text may be outlined or the figure rasterized; check that text is selectable (TF-50)")
    warns = judge(eff_pt, None, args)
    for x in warns:
        lines.append(f"  - WARN {x}")
    return len(warns) + len(unemb) + len(t3)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*")
    ap.add_argument("--docx", help="check every image embedded in this docx at its displayed width")
    ap.add_argument("--print-width", type=float, default=None, help="final printed width in inches (default 6.5)")
    ap.add_argument("--design-width", type=float, default=None, help="width the figure was designed at, inches")
    ap.add_argument("--font-pt", type=float, default=9.0, help="font size used at design size (default 9)")
    ap.add_argument("--min-pt", type=float, default=9.0)
    ap.add_argument("--min-dpi", type=float, default=300.0)
    ap.add_argument("--out")
    args = ap.parse_args()
    args.print_width_given = args.print_width is not None
    if args.print_width is None:
        args.print_width = 6.5
    if not args.files and not args.docx:
        ap.error("give figure files and/or --docx")

    lines = ["# Figure check", "",
             f"Settings: design font {args.font_pt:g} pt, minimum {args.min_pt:g} pt, minimum {args.min_dpi:g} dpi; "
             f"Pillow {'available' if Image else 'NOT installed'}, pdfinfo {'yes' if shutil.which('pdfinfo') else 'no'}, "
             f"pdffonts {'yes' if shutil.which('pdffonts') else 'no'}.", ""]
    warns = 0
    if args.docx:
        from docx_text import image_extents
        ext = image_extents(args.docx)
        lines.append(f"## Images embedded in {os.path.basename(args.docx)}: {len(ext)}")
        with tempfile.TemporaryDirectory() as tmp, zipfile.ZipFile(args.docx) as z:
            for i, (target, wi, hi) in enumerate(ext, 1):
                name = "word/" + target if not target.startswith("word/") else target
                try:
                    data = z.read(name)
                except KeyError:
                    lines.append(f"- image {i}: {target} not found in the package")
                    continue
                p = os.path.join(tmp, os.path.basename(target))
                with open(p, "wb") as fh:
                    fh.write(data)
                warns += report_image(p, f"image {i} ({os.path.basename(target)}, shown {wi:.2f} x {hi:.2f} in)", wi, args, lines)
        lines.append("")
    if args.files:
        lines.append("## Files")
        for f in args.files:
            if f.lower().endswith(".pdf"):
                warns += report_pdf(f, None, args, lines)
            else:
                warns += report_image(f, os.path.basename(f), None, args, lines)
    lines.insert(2, f"Summary: {warns} warnings.")
    rep = "\n".join(lines)
    print(rep)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(rep + "\n")
    return 1 if warns else 0


if __name__ == "__main__":
    sys.exit(main())
