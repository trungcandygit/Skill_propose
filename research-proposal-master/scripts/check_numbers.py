#!/usr/bin/env python3
"""List every decimal number in a .docx and flag those not found in the CSV outputs.

Why: numbers in prose drift from the tables during revision, and the letter
quotes numbers that were never re-read from the output files (core C-07,
seat2 card S2-02, S2-10). Matching each printed decimal against the values the
code actually wrote is mechanical, so the script does all of them; nothing is
sampled (core C-61).

How a number matches: a printed value with d decimals matches a CSV value v
if round(v, d) equals it within --tol (default: half a unit in the last digit),
also trying |v| (sign narrated in words), 100·v (shares printed as percent) and
v/100. Integers are skipped unless --integers is given (years, Ns and table
numbers make integer matching noisy). Values in the reference list are skipped.

Output: a summary, then every unmatched number with its location and context,
then (with --all) every matched number with the CSV file and cell it matched.
An unmatched number is not automatically wrong: it may come from an output not
exported to CSV, a hand calculation, or an external source. Each one needs a
named source before the paper goes out.

Usage
  python3 check_numbers.py paper.docx CSV_FOLDER [--out report.md] [--tol 0.0005]
         [--all] [--integers] [--skip-tables] [--min-decimals 1]

Standard library only. Exit code 1 if any number is unmatched.
"""
import argparse
import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx_text import read_blocks, reference_split, is_heading  # noqa: E402

NUMRE = re.compile(r"(?<![\w.])([−\-–]?)(\d{1,3}(?:,\d{3})+|\d+)(?:\.(\d+))?(%?)(?![\w])")


def load_csv_values(folder):
    vals = []  # (value, file, row, col)
    for root, _, files in os.walk(folder):
        for f in sorted(files):
            if not f.lower().endswith(".csv"):
                continue
            path = os.path.join(root, f)
            try:
                with open(path, newline="", encoding="utf-8-sig") as fh:
                    rows = list(csv.reader(fh))
            except (OSError, UnicodeDecodeError):
                continue
            header = rows[0] if rows else []
            for i, row in enumerate(rows[1:], start=2):
                for j, cell in enumerate(row):
                    c = cell.strip().replace(",", "")
                    try:
                        v = float(c)
                    except ValueError:
                        for m in re.finditer(r"-?\d+(?:\.\d+)?(?:e-?\d+)?", c):
                            try:
                                vals.append((float(m.group()), os.path.relpath(path, folder), i, header[j] if j < len(header) else j))
                            except ValueError:
                                pass
                        continue
                    vals.append((v, os.path.relpath(path, folder), i, header[j] if j < len(header) else j))
    return vals


def build_index(vals, max_dec=6):
    """Map (decimals, rounded string) -> first source, for fast lookup."""
    idx = {}
    for v, f, r, c in vals:
        for transform, tag in ((v, ""), (abs(v), "abs"), (v * 100, "x100"), (abs(v) * 100, "abs x100"), (v / 100, "/100")):
            for d in range(0, max_dec + 1):
                key = (d, f"{round(transform, d):.{d}f}")
                idx.setdefault(key, (f, r, c, v, tag))
    return idx


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("docx")
    ap.add_argument("csv_folder")
    ap.add_argument("--out")
    ap.add_argument("--tol", type=float, default=None, help="absolute tolerance; default half a unit in the last printed digit")
    ap.add_argument("--all", action="store_true", help="also list matched numbers with their source cell")
    ap.add_argument("--integers", action="store_true", help="also check integers with thousands separators (e.g. N = 1,891)")
    ap.add_argument("--skip-tables", action="store_true", help="check prose only, not table cells")
    ap.add_argument("--min-decimals", type=int, default=1)
    args = ap.parse_args()

    vals = load_csv_values(args.csv_folder)
    if not vals:
        sys.exit(f"No numeric CSV values found under {args.csv_folder}")
    idx = build_index(vals)
    blocks, _ = reference_split(read_blocks(args.docx))
    blocks = [b for b in blocks if not is_heading(b)]
    if args.skip_tables:
        blocks = [b for b in blocks if b["kind"] != "cell"]

    found, missing = [], []
    for b in blocks:
        t = b["text"]
        for m in NUMRE.finditer(t):
            sign, whole, dec, pct = m.groups()
            if dec is None:
                if not (args.integers and "," in whole):
                    continue
                dec = ""
            if len(dec) < args.min_decimals and not (args.integers and "," in whole):
                continue
            # skip things that look like dates, versions, section numbers ("4.2" right after "Section")
            pre = t[max(0, m.start() - 12):m.start()].lower()
            if re.search(r"(section|sections|table|figure|appendix|equation|eq\.|version|v)\s*$", pre):
                continue
            num = float(whole.replace(",", "") + ("." + dec if dec else ""))
            neg = sign in ("-", "−", "–") and (m.start() == 0 or not t[m.start() - 1].isdigit())
            val = -num if neg else num
            d = len(dec)
            key = (d, f"{round(val, d):.{d}f}")
            hit = idx.get(key) or idx.get((d, f"{round(abs(val), d):.{d}f}"))
            if hit is None and args.tol:
                for v, f, r, c in vals:
                    if abs(abs(v) - abs(val)) <= args.tol or abs(abs(v * 100) - abs(val)) <= args.tol:
                        hit = (f, r, c, v, "tol")
                        break
            a, z = max(0, m.start() - 60), min(len(t), m.end() + 60)
            ctx = t[a:m.start()] + "[[" + t[m.start():m.end()] + "]]" + t[m.end():z]
            loc = f"table {b['table']}" if b["kind"] == "cell" else f"{b['kind']} {b['index']}"
            (found if hit else missing).append((m.group(0), loc, ctx, hit))

    lines = [f"# Number check: {os.path.basename(args.docx)} against {args.csv_folder}", "",
             f"Summary: {len(found) + len(missing)} decimal numbers checked; {len(found)} matched a CSV value; "
             f"{len(missing)} unmatched; {len(vals)} CSV values from the folder.",
             f"Weak matches (1 printed decimal, or matched only after a x100, /100 or sign transform; coincidence is likely): "
             f"{sum(1 for n, _, _, h in found if len(n.split('.')[-1].rstrip('%')) <= 1 or h[4])}. Check these by hand.", ""]
    by_loc = {}
    for n, loc, ctx, _ in missing:
        by_loc.setdefault(loc.split()[0], []).append(1)
    lines.append("Unmatched by location: " + ", ".join(f"{k}={len(v)}" for k, v in by_loc.items()))
    lines.append("")
    lines.append("## Unmatched numbers (need a named source: an output file, a calculation, or a citation)")
    for n, loc, ctx, _ in missing:
        lines.append(f"- {n} | {loc} | {ctx}")
    if args.all:
        lines.append("")
        lines.append("## Matched numbers")
        for n, loc, ctx, (f, r, c, v, tag) in found:
            lines.append(f"- {n} | {loc} | {f} row {r} col {c} = {v:.6g}{(' (' + tag + ')') if tag else ''}")
    rep = "\n".join(lines)
    print(rep)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(rep + "\n")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
