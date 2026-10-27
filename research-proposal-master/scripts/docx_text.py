#!/usr/bin/env python3
"""Shared reader for the check scripts: turns a .docx into a list of blocks.

Why a custom reader: python-docx skips footnotes, does not tell you whether a
paragraph sits inside a table, and is not always installed. Reading the XML in
the zip with the standard library works everywhere and keeps the scripts
dependency-free.

Each block is a dict:
    kind     "p" (body paragraph) | "cell" (table cell paragraph) | "footnote"
    text     plain text (tabs and breaks become spaces)
    style    paragraph style id (e.g. "Heading1", "Caption") or ""
    italic   share of characters in italic runs (0..1), used to skip quotes
    math     True if the paragraph holds an Office Math object
    index    running position, used as a location in reports
    table    table number (1-based) for kind == "cell", else None

Run directly to dump the blocks:  python3 docx_text.py paper.docx
"""
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"


def _par_text(p):
    parts, italic_chars, total = [], 0, 0
    for node in p.iter():
        tag = node.tag
        if tag == W + "r":
            rpr = node.find(W + "rPr")
            is_it = rpr is not None and rpr.find(W + "i") is not None and \
                rpr.find(W + "i").get(W + "val", "true") not in ("0", "false")
            txt = "".join(
                (t.text or "") if t.tag == W + "t" else " "
                for t in node if t.tag in (W + "t", W + "tab", W + "br")
            )
            parts.append(txt)
            total += len(txt)
            if is_it:
                italic_chars += len(txt)
        elif tag == M + "t":
            parts.append(node.text or "")
    text = re.sub(r"\s+", " ", "".join(parts)).strip()
    return text, (italic_chars / total if total else 0.0)


def _style(p):
    ppr = p.find(W + "pPr")
    if ppr is None:
        return ""
    st = ppr.find(W + "pStyle")
    return st.get(W + "val", "") if st is not None else ""


def read_blocks(path):
    with zipfile.ZipFile(path) as z:
        body = ET.fromstring(z.read("word/document.xml")).find(W + "body")
        foot = None
        if "word/footnotes.xml" in z.namelist():
            foot = ET.fromstring(z.read("word/footnotes.xml"))
    blocks, idx, tcount = [], 0, 0

    def add(p, kind, table=None):
        nonlocal idx
        text, ital = _par_text(p)
        if not text:
            return
        idx += 1
        blocks.append({
            "kind": kind, "text": text, "style": _style(p), "italic": ital,
            "math": p.find(".//" + M + "oMath") is not None, "index": idx,
            "table": table,
        })

    for child in body:
        if child.tag == W + "p":
            add(child, "p")
        elif child.tag == W + "tbl":
            tcount += 1
            for p in child.iter(W + "p"):
                add(p, "cell", tcount)
        elif child.tag == W + "sdt":
            for p in child.iter(W + "p"):
                add(p, "p")
    if foot is not None:
        for fn in foot.findall(W + "footnote"):
            if fn.get(W + "type") in ("separator", "continuationSeparator"):
                continue
            for p in fn.iter(W + "p"):
                add(p, "footnote")
    return blocks


def is_heading(b):
    return b["kind"] == "p" and (b["style"].lower().startswith("heading") or b["style"].lower() == "title")


def reference_split(blocks):
    """Return (body_blocks, reference_blocks) split at a References heading."""
    for i, b in enumerate(blocks):
        if b["kind"] == "p" and re.fullmatch(r"(\d+\.?\s*)?(references|bibliography|reference list|works cited)", b["text"].strip().lower()):
            rest = blocks[i + 1:]
            refs = []
            for r in rest:
                if is_heading(r) and refs:
                    break
                if r["kind"] == "p":
                    refs.append(r)
            after = rest[len(refs):]
            return blocks[:i] + after, refs
    return blocks, []


def image_extents(path):
    """Embedded images with their displayed size: [(media_name, width_in, height_in)]."""
    out = []
    ns_a = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
    ns_r = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
    ns_wp = "{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}"
    with zipfile.ZipFile(path) as z:
        doc = ET.fromstring(z.read("word/document.xml"))
        rels = ET.fromstring(z.read("word/_rels/document.xml.rels"))
        rmap = {r.get("Id"): r.get("Target") for r in rels}
        for drawing in doc.iter(W + "drawing"):
            ext = drawing.find(".//" + ns_wp + "extent")
            blip = drawing.find(".//" + ns_a + "blip")
            if ext is None or blip is None:
                continue
            target = rmap.get(blip.get(ns_r + "embed"), "")
            out.append((target, int(ext.get("cx")) / 914400.0, int(ext.get("cy")) / 914400.0))
    return out


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    for b in read_blocks(sys.argv[1]):
        flag = "M" if b["math"] else " "
        print(f"{b['index']:5d} {b['kind']:8s} {b['style'][:12]:12s} {flag} {b['text'][:150]}")
