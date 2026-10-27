#!/usr/bin/env python3
"""Build a read-only text dossier for panel agents from .docx files.

Usage: python3 make_dossier.py OUT_DIR NAME=path.docx [NAME=path.docx ...] [--copy path ...]
Each docx is dumped in body order (paragraphs and table rows, cells joined by ' | ') to OUT_DIR/NAME.txt,
so agents can grep and quote line numbers. --copy copies other files (comments, PDFs) unchanged.
Typical: manuscript_REVISED_clean, manuscript_ORIGINAL, response_letter, plus the verbatim comments.
Never pass the writer's own verdicts or earlier panel reports (panel independence, orchestrator O-30).
"""
import os, shutil, sys
import docx
from docx.table import Table
from docx.text.paragraph import Paragraph


def dump(src, dst):
    d = docx.Document(src); out = []
    for el in d.element.body.iterchildren():
        if el.tag.endswith("}p"):
            out.append(Paragraph(el, d).text)
        elif el.tag.endswith("}tbl"):
            out += [" | ".join(c.text for c in r.cells) for r in Table(el, d).rows]
    open(dst, "w", encoding="utf-8").write("\n".join(out))


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__); return
    out = argv[1]; os.makedirs(out, exist_ok=True)
    args = argv[2:]; copy = False
    for a in args:
        if a == "--copy":
            copy = True; continue
        if copy:
            shutil.copy(a, out)
        else:
            name, path = a.split("=", 1); dump(path, os.path.join(out, name + ".txt"))
    print("\n".join(sorted(os.listdir(out))))


main(sys.argv)
