#!/usr/bin/env python3
"""Cross-reference and citation two-way check for a .docx manuscript.

Why: revisions renumber exhibits and sections and add or drop references, and
the result ("see Table 6" pointing at nothing, a reference never cited, a 2020
paper cited as 2019) is exactly what referees notice (seat2 card S2-06, S2-79).
These are yes/no checks, so a script does them completely.

Checks
  1. Tables, figures, appendix tables/figures: every mention ("Table 3",
     "Tables 2 and 4", "Table A4", "Figure 1", "Fig. 2", "Tables A1 to A3")
     has a caption paragraph ("Table 3 ..."), and every captioned exhibit is
     mentioned outside its own caption. Also flags exhibits first mentioned out
     of order and duplicate caption numbers.
  2. Sections and appendices: "Section 4.2", "Appendix B" exist as numbered
     headings (or appendix headings / captions).
  3. Equations: "equation (5)", "Eq. (5)", "eqs. (2)-(3)" exist as a numbered
     display equation "(5)" at the end of a math paragraph; numbered equations
     never referenced are listed.
  4. Citations: author-year citations in the text ("Smith (2020)",
     "(Smith & Lee, 2019a; Wang et al., 2021)") are matched two-way against the
     reference list by first-author surname and year.

Usage
  python3 check_crossrefs.py paper.docx [--out report.md]

Standard library only. Exit code 1 if any mention points to a missing object
or any citation fails to match.
"""
import argparse
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx_text import read_blocks, reference_split, is_heading  # noqa: E402

NUM = r"[A-Z]?\d+[a-z]?"
EXH = re.compile(r"\b(Tables?|Figures?|Figs?\.)\s+(" + NUM + r"(?:\s*(?:,|and|&|to|–|-)\s*" + NUM + r")*)")
CAP = re.compile(r"^(Table|Figure|Fig\.)\s+(" + NUM + r")\b[.:]?\s+\S")


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def expand(spec):
    """'A1 to A3' -> [A1, A2, A3]; '2 and 4' -> [2, 4]."""
    spec = re.sub(r"\b(Tables?|Figures?)\s+", "", spec)
    items = re.split(r"\s*(?:,|and|&)\s*", spec)
    out = []
    for it in items:
        m = re.match(r"^(" + NUM + r")\s*(?:to|–|-)\s*(" + NUM + r")$", it.strip())
        if m:
            a, b = m.groups()
            pa, na = re.match(r"([A-Z]?)(\d+)", a).groups()
            pb, nb = re.match(r"([A-Z]?)(\d+)", b).groups()
            if pa == pb and int(nb) >= int(na) and int(nb) - int(na) < 40:
                out += [f"{pa}{i}" for i in range(int(na), int(nb) + 1)]
                continue
            out += [a, b]
        elif it.strip():
            out.append(it.strip())
    return out


def kind_of(word):
    return "Table" if word.lower().startswith("tab") else "Figure"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("docx")
    ap.add_argument("--out")
    args = ap.parse_args()

    blocks = read_blocks(args.docx)
    body, refs = reference_split(blocks)
    lines = [f"# Cross-reference check: {os.path.basename(args.docx)}", ""]
    fails = 0

    # ---- exhibits
    captions, cap_blocks = {}, set()
    for b in body:
        m = CAP.match(b["text"])
        if m and re.match(r"^\S+\s+\S+\s+(reports?|shows?|presents?|compares?|lists?|provides?|summari[sz]es|displays?|plots?|gives?|contains?|repeats?|adds?|uses?)\b", b["text"]):
            m = None  # a sentence about the exhibit, not its caption
        if m and b["kind"] in ("p", "cell") and len(b["text"]) < 400:
            key = (kind_of(m.group(1)), m.group(2))
            captions.setdefault(key, []).append(b["index"])
            cap_blocks.add(b["index"])
    mentions = {}
    order = []
    for b in body:
        if b["index"] in cap_blocks:
            continue
        for m in EXH.finditer(b["text"]):
            k = kind_of(m.group(1))
            for n in expand(m.group(2)):
                mentions.setdefault((k, n), []).append(b["index"])
                order.append((k, n, b["index"]))
    missing = sorted(k for k in mentions if k not in captions)
    unref = sorted(k for k in captions if k not in mentions)
    dup = sorted(k for k, v in captions.items() if len(v) > 1)
    lines.append(f"## 1. Tables and figures: {len(captions)} captions, {len(mentions)} distinct mentions")
    lines.append(f"- Mentioned but no caption found ({len(missing)}): " + (", ".join(f"{k} {n} (blocks {mentions[(k, n)][:5]})" for k, n in missing) or "none"))
    lines.append(f"- Captioned but never mentioned in the text ({len(unref)}): " + (", ".join(f"{k} {n}" for k, n in unref) or "none"))
    lines.append(f"- Duplicate caption numbers ({len(dup)}): " + (", ".join(f"{k} {n} at blocks {captions[(k, n)]}" for k, n in dup) or "none"))
    seen, ooo = {"Table": [], "Figure": []}, []
    for k, n, idx in order:
        if not n.isdigit():
            continue
        lst = seen[k]
        if int(n) not in lst:
            if lst and int(n) < max(lst) and int(n) - 1 not in lst and int(n) != 1:
                ooo.append(f"{k} {n} first mentioned at block {idx} after {k} {max(lst)}")
            lst.append(int(n))
    for k in ("Table", "Figure"):
        nums = sorted(int(n) for kk, n in captions if kk == k and n.isdigit())
        gaps = [i for i in range(1, (max(nums) if nums else 0) + 1) if i not in nums]
        if gaps:
            ooo.append(f"{k} numbering has gaps: missing {gaps}")
    lines.append(f"- Order and numbering issues ({len(ooo)}): " + ("; ".join(ooo) or "none"))
    fails += len(missing) + len(dup)
    lines.append("")

    # ---- sections and appendices
    heads = [b for b in body if is_heading(b)]
    sec_nums, app_names = set(), set()
    for h in heads:
        m = re.match(r"^(\d+(?:\.\d+)*)\.?\s", h["text"])
        if m:
            sec_nums.add(m.group(1))
        m = re.match(r"^(?:Online\s+)?Appendix\s+([A-Z0-9]+)\b", h["text"], re.I)
        if m:
            app_names.add(m.group(1).upper())
    for b in body:  # appendix tables imply appendix existence
        m = CAP.match(b["text"])
        if m and m.group(2)[0].isalpha():
            app_names.add(m.group(2)[0])
    has_appendix_heading = any(re.match(r"^(online\s+)?appendix", h["text"], re.I) for h in heads)
    sref, aref = {}, {}
    for b in body:
        if is_heading(b):
            continue
        for m in re.finditer(r"\bSections?\s+(\d+(?:\.\d+)*)(?:\s*(?:and|,|to|–|-)\s*(\d+(?:\.\d+)*))?", b["text"]):
            for g in m.groups():
                if g:
                    sref.setdefault(g, []).append(b["index"])
        for m in re.finditer(r"\bAppendix\s+(?!Tables?|Figures?)([A-Z]\d?|\d+)\b", b["text"]):
            aref.setdefault(m.group(1).upper(), []).append(b["index"])
    smiss = sorted(s for s in sref if s not in sec_nums)
    amiss = sorted(a for a in aref if a not in app_names and a[0] not in app_names)
    lines.append(f"## 2. Sections and appendices: {len(sec_nums)} numbered headings, {len(sref)} section mentions, {len(aref)} appendix mentions")
    lines.append(f"- Section mentions with no heading ({len(smiss)}): " + (", ".join(f"Section {s} (blocks {sref[s][:5]})" for s in smiss) or "none"))
    lines.append(f"- Appendix mentions with no appendix heading or appendix exhibit ({len(amiss)}): " + (", ".join(f"Appendix {a} (blocks {aref[a][:5]})" for a in amiss) or "none"))
    if aref and not has_appendix_heading:
        lines.append("- Note: no heading starting with 'Appendix' was found; appendix exhibits exist only as captions.")
    fails += len(smiss) + len(amiss)
    lines.append("")

    # ---- equations
    eq_nums = {}
    for b in body:
        m = re.search(r"\((\d+[a-z]?)\)\s*$", b["text"])
        if m and (b["math"] or len(b["text"]) < 160 and "=" in b["text"]):
            eq_nums.setdefault(m.group(1), b["index"])
    eref = {}
    for b in body:
        if b["math"]:
            continue
        for m in re.finditer(r"\b(?:[Ee]quations?|[Ee]qs?\.)\s*((?:\(\d+[a-z]?\)(?:\s*(?:,|and|to|–|-)\s*)?)+)", b["text"]):
            nums = re.findall(r"\((\d+[a-z]?)\)", m.group(1))
            if re.search(r"\)\s*(?:to|–|-)\s*\(", m.group(1)) and len(nums) == 2 and nums[0].isdigit() and nums[1].isdigit():
                nums = [str(i) for i in range(int(nums[0]), int(nums[1]) + 1)]
            for n in nums:
                eref.setdefault(n, []).append(b["index"])
    emiss = sorted((n for n in eref if n not in eq_nums), key=lambda x: int(re.match(r"\d+", x).group()))
    eunref = sorted((n for n in eq_nums if n not in eref), key=lambda x: int(re.match(r"\d+", x).group()))
    lines.append(f"## 3. Equations: {len(eq_nums)} numbered, {len(eref)} referenced")
    lines.append(f"- Referenced but not found ({len(emiss)}): " + (", ".join(f"({n}) at blocks {eref[n][:5]}" for n in emiss) or "none"))
    lines.append(f"- Numbered but never referenced ({len(eunref)}): " + (", ".join(f"({n})" for n in eunref) or "none"))
    fails += len(emiss)
    lines.append("")

    # ---- citations
    ref_keys = {}
    for r in refs:
        t = r["text"]
        m = re.match(r"^\s*([A-Z][^\s,(]*(?:[\s\-][a-z]{1,3}\s[A-Z][^\s,(]*)?(?:[\s\-][A-Z][a-z]+)?)\s*,", t) or re.match(r"^\s*([^\s,(]+)", t)
        y = re.search(r"\((\d{4}[a-z]?|n\.d\.|in press|forthcoming)\)|\b((?:19|20)\d{2}[a-z]?)\b", t)
        if m and y:
            surname = norm(m.group(1).split()[-1] if m.group(1).split()[0].islower() else m.group(1))
            year = (y.group(1) or y.group(2)).lower()
            ref_keys.setdefault((surname, year), []).append(t[:90])
    author = r"(?:[A-Z][\w'’\-]+(?:\s(?:van|von|de|der|da|di|le|la)\s[A-Z][\w'’\-]+)?)"
    tail = r"(?:\s+et\s+al\.?|\s*(?:,|&|and)\s*" + author + r"(?:\s*(?:,|&|and)\s*" + author + r")*)?"
    narrative = re.compile(r"\b(" + author + r")" + tail + r"\s*\((\d{4}[a-z]?)(?:[,;][^)]*)?\)")
    paren = re.compile(r"\(([^()]*\b(?:19|20)\d{2}[a-z]?[^()]*)\)")
    item = re.compile(r"(" + author + r")" + tail + r",?\s+((?:19|20)\d{2}[a-z]?)")
    cites = {}
    for b in body:
        if b["kind"] not in ("p", "footnote", "cell"):
            continue
        t = unicodedata.normalize("NFKD", b["text"])
        t = "".join(c for c in t if not unicodedata.combining(c))
        for m in narrative.finditer(t):
            cites.setdefault((norm(m.group(1)), m.group(2).lower()), []).append(b["index"])
        for m in paren.finditer(t):
            for part in re.split(r";", m.group(1)):
                for mm in item.finditer(part):
                    cites.setdefault((norm(mm.group(1)), mm.group(2).lower()), []).append(b["index"])
                # "Smith, 2019, 2020" extra years
                if mm := item.search(part):
                    for extra in re.findall(r",\s*((?:19|20)\d{2}[a-z]?)\b", part[mm.end():]):
                        cites.setdefault((norm(mm.group(1)), extra.lower()), []).append(b["index"])
    stop = {"table", "figure", "section", "appendix", "equation", "january", "february", "march", "april", "may",
            "june", "july", "august", "september", "october", "november", "december", "fy", "covid", "since",
            "in", "the", "from", "until", "before", "after", "during", "between"}
    cites = {k: v for k, v in cites.items() if k[0] not in stop and len(k[0]) > 1}

    def find(key, pool):
        if key in pool:
            return key
        s, y = key
        for (s2, y2) in pool:
            if y2 == y and (s2.startswith(s) or s.startswith(s2) or s2.split()[-1] == s.split()[-1]):
                return (s2, y2)
        return None

    nomatch = sorted(k for k in cites if not find(k, ref_keys))
    uncited = sorted(k for k in ref_keys if not find(k, cites))
    near = []
    for s, y in nomatch:
        alts = [f"{s2} {y2}" for (s2, y2) in ref_keys if s2 == s]
        if alts:
            near.append(f"{s} {y} -> reference list has {', '.join(alts)}")
    lines.append(f"## 4. Citations: {len(cites)} distinct in-text author-year keys, {len(ref_keys)} reference entries parsed (of {len(refs)} reference paragraphs)")
    lines.append(f"- Cited in text but not in the reference list ({len(nomatch)}): " + (", ".join(f"{s.title()} {y} (blocks {cites[(s, y)][:3]})" for s, y in nomatch) or "none"))
    lines.append(f"- Likely year mismatches ({len(near)}): " + ("; ".join(near) or "none"))
    lines.append(f"- In the reference list but never cited ({len(uncited)}): " + (", ".join(f"{s.title()} {y}" for s, y in uncited) or "none"))
    unparsed = len(refs) - sum(len(v) for v in ref_keys.values())
    if unparsed > 0:
        lines.append(f"- Reference paragraphs not parsed (check by hand): {unparsed}")
    fails += len(nomatch) + len(uncited)
    lines.append("")
    lines.insert(2, f"Summary: {fails} hard failures (missing targets, duplicate captions, unmatched citations).")
    lines.insert(3, "")
    rep = "\n".join(lines)
    print(rep)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(rep + "\n")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
