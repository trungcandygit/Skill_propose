#!/usr/bin/env python3
"""Mechanical style gate for a .docx manuscript or response letter.

Why: "I re-read it and it looks fine" is not an audit (seat1 card S1-89). These
checks are deterministic, so a script finds every instance and reports counts
that a reviewer can verify. The script only reports; deciding whether a hit is
acceptable (for example a causal verb in a well-identified design) stays with
the author and the panel.

Checks
  1. Dashes: em dash (—), spaced en dash used as a dash ( – ), and en dash in
     prose that is not a number range. Rule S1-80: zero em dashes in new prose.
  2. Banned phrases: throat-clearing, AI vocabulary, intensifiers, forbidden
     letter phrases (stop-slop, econ-write, humanizer_academic, nature-response).
  3. Causal wording: "effect of", "impact", "causes", "drives", "leads to",
     "increases/reduces/raises/lowers" ... shown with context, so the author can
     check each against the design (core C-20, C-21).
  4. Acronyms: an all-caps token used before (or without) a definition of the
     form "Full Term (ACR)" (S1-69). Heuristic; use --allow to whitelist.
  5. Note length: "Note:"/"Notes:" paragraphs longer than --max-note-sentences (2) or --max-note-words (30)
     (default 2, user rule TF-15).

Usage
  python3 check_docx_style.py paper.docx [--out report.md] [--skip-italic]
         [--allow GRI,ESG] [--max-note-sentences 2] [--no-references]

--skip-italic skips paragraphs that are mostly italic (quoted reviewer
comments in a response letter). Standard library only; exit code 1 if any em
dash or banned phrase is found.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx_text import is_heading, read_blocks, reference_split  # noqa: E402

BANNED = [
    # throat-clearing and meta-commentary (stop-slop phrases.md, econ-write)
    "it is important to note", "it should be noted", "it is worth noting", "it's worth noting",
    "it is worth mentioning", r"re:(?:^|[.!?]\s+)note that", "in this section, we", "in this section we",
    "here's what", "here's why", "let me walk you through", "as we'll see", "the rest of this paper",
    "at its core", "at the end of the day", "when it comes to", "in a world where", "the reality is",
    "the truth is", "it turns out", "make no mistake", "let that sink in", "this matters because",
    "one can see that", "in order to", "the fact that",
    # vague declaratives and cheerleading (stop-slop, master-academic-paper-skill)
    "the implications are significant", "the stakes are high", "plays a key role", "plays a crucial role",
    "plays a pivotal role", "serves to highlight", "sheds light on", "shed light on", "paves the way",
    "pave the way", "a testament to",
    # AI vocabulary (econ-write banned words, humanizer_academic)
    "delve", "delves", "landscape", "multifaceted", "pivotal", "crucial", "groundbreaking", "intricate",
    "interplay", "holistic", "underscore", "underscores", "garner", "foster", "fosters",
    "re:\\bleverag(?:e|es|ed|ing)\\s+(?:the|our|this|these|its|their|a|an)\\b", "utilize", "utilizes", "utilization", "tapestry", "realm", "showcase", "showcasing",
    "navigate the", "unpack", "deep dive", "game-changer", "paramount", "poised to",
    # intensifiers (proofreading, stop-slop)
    "very", "quite", "really", "truly", "simply", "deeply", "extremely", "highly significant",
    "very significant", "striking",
    # forbidden in response letters (nature-response tone-and-stance, aer-rebuttal)
    "the reviewer misunderstood", "the reviewer is wrong", "we believe this is sufficient",
    "we have revised accordingly", "as everyone knows", "due to lack of funding", "as we already said",
    "as should be clear from", "we will consider", "thank you for the comment.",
]

CAUSAL = [
    r"effects? of", r"impacts?", r"impacted", r"causes?", r"caused", r"causal", r"drives?", r"driven by",
    r"leads? to", r"led to", r"results? in", r"increases", r"increased", r"reduces", r"reduced",
    r"raises", r"lowers", r"boosts?", r"improves", r"worsens", r"determines", r"affects", r"affected",
    r"influences?", r"contributes? to", r"because of",
]

ACR_STOP = {"I", "A", "AND", "OR", "THE", "OF", "IN", "TO", "NOTE", "SOURCE", "TABLE", "FIGURE",
            "II", "III", "IV", "VI", "VII", "VIII", "IX", "XI", "XII", "AUTHORS", "COMPLETE", "AUTHOR",
            "INPUT", "NEEDED", "FY", "VS", "USD", "VND", "COVID", "PDF", "DOI", "URL", "ORCID"}


def sentences(text):
    return [s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z(\"'*])", text.strip()) if s]


def context(text, start, end, width=70):
    a, b = max(0, start - width), min(len(text), end + width)
    return ("..." if a else "") + text[a:start] + "[[" + text[start:end] + "]]" + text[end:b] + ("..." if b < len(text) else "")


def where(b):
    if b["kind"] == "cell":
        return f"table {b['table']} cell (block {b['index']})"
    return f"{b['kind']} {b['index']}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("docx")
    ap.add_argument("--out", help="write the report (markdown) here as well as to stdout")
    ap.add_argument("--skip-italic", action="store_true", help="skip paragraphs that are >60%% italic (quoted comments)")
    ap.add_argument("--allow", default="", help="comma-separated acronyms that need no definition")
    ap.add_argument("--max-note-sentences", type=int, default=2)
    ap.add_argument("--max-note-words", type=int, default=30, help="user rule: notes stay short; flag notes longer than this many words")
    ap.add_argument("--no-references", action="store_true", help="also scan the reference list")
    args = ap.parse_args()

    blocks = read_blocks(args.docx)
    if not args.no_references:
        blocks, _ = reference_split(blocks)
    if args.skip_italic:
        blocks = [b for b in blocks if b["italic"] <= 0.6]
    prose = [b for b in blocks if b["kind"] in ("p", "footnote") and not b["math"]]

    out = [f"# Style check: {os.path.basename(args.docx)}", ""]
    counts = {}

    # 1 dashes
    dash_hits = []
    for b in blocks:
        t = b["text"]
        for m in re.finditer("—", t):
            dash_hits.append(("em dash", b, m))
        for m in re.finditer(r"\s–\s", t):
            dash_hits.append(("spaced en dash (used as a dash)", b, m))
        for m in re.finditer(r"(?<![\d\s])–(?![\d])", t):
            dash_hits.append(("en dash in prose", b, m))
        for m in re.finditer(r"(?<=\w)---(?=\w)|\s--\s", t):
            dash_hits.append(("typed dash (--- or --)", b, m))
    counts["dashes"] = len(dash_hits)
    out.append(f"## 1. Dashes: {len(dash_hits)} (em dash: {sum(1 for k, _, _ in dash_hits if k == 'em dash')})")
    for kind, b, m in dash_hits:
        out.append(f"- {kind} | {where(b)} | {context(b['text'], m.start(), m.end())}")
    out.append("")

    # 2 banned phrases
    hits = []
    for b in prose + [x for x in blocks if x["kind"] == "cell"]:
        low = b["text"].lower()
        for ph in BANNED:
            rx = ph[3:] if ph.startswith("re:") else r"(?<![\w-])" + re.escape(ph) + r"(?![\w-])"
            for m in re.finditer(rx, low):
                hits.append((ph.replace("re:", ""), b, m))
    counts["banned"] = len(hits)
    out.append(f"## 2. Banned phrases: {len(hits)}")
    tally = {}
    for ph, _, _ in hits:
        tally[ph] = tally.get(ph, 0) + 1
    if tally:
        out.append("Counts: " + ", ".join(f"{k} ×{v}" for k, v in sorted(tally.items(), key=lambda x: -x[1])))
    for ph, b, m in hits:
        out.append(f"- \"{ph}\" | {where(b)} | {context(b['text'], m.start(), m.end())}")
    out.append("")

    # 3 causal wording
    pat = re.compile(r"\b(" + "|".join(CAUSAL) + r")\b", re.I)
    chits = []
    for b in prose:
        for m in pat.finditer(b["text"]):
            pre = b["text"][max(0, m.start() - 40):m.start()].lower()
            if re.search(r"associated with( an?| the)?\s*$|correlat\w* with\s*$", pre):
                continue  # already worded as an association
            tag = " [negated]" if re.search(r"\b(not|no|nor|without)\b[^.]{0,40}$", pre) else ""
            chits.append((m.group(1).lower() + tag, b, m))
    counts["causal"] = len(chits)
    out.append(f"## 3. Causal wording to check against the design: {len(chits)}")
    out.append("Each hit is fine only if the design identifies a causal effect (core C-21); otherwise rewrite as an association (C-20).")
    for w, b, m in chits:
        out.append(f"- {w} | {where(b)} | {context(b['text'], m.start(), m.end())}")
    out.append("")

    # 4 acronyms
    allow = {a.strip().upper() for a in args.allow.split(",") if a.strip()}
    defined, first_use, problems = {}, {}, []
    defn = re.compile(r"\b([A-Z][A-Za-z'\-]+(?:[\s\-]+(?:of|and|for|the|in|on|to|[A-Z][A-Za-z'\-]+)){0,7})\s+\(([A-Z][A-Z0-9&\-]{1,9}s?)\)")
    token = re.compile(r"\b([A-Z][A-Z0-9&\-]{1,9})s?\b")
    for b in prose:
        t = b["text"]
        for m in defn.finditer(t):
            defined.setdefault(m.group(2).rstrip("s"), b["index"])
        for m in re.finditer(r"\(([A-Z][A-Z0-9&\-]{1,9})s?(?:[;,][^)]*)?\)", t):
            pass
        for m in token.finditer(t):
            tok = m.group(1)
            if tok in ACR_STOP or tok in allow or len(tok) < 2 or tok.isdigit():
                continue
            if not re.search(r"[A-Z]{2}", tok):
                continue
            first_use.setdefault(tok, (b, m))
    for tok, (b, m) in sorted(first_use.items(), key=lambda x: x[1][0]["index"]):
        d = defined.get(tok)
        if d is None:
            problems.append(f"- {tok}: never defined as 'Full term ({tok})' | first use {where(b)} | {context(b['text'], m.start(), m.end(), 50)}")
        elif d > b["index"]:
            problems.append(f"- {tok}: used at {where(b)} before its definition at block {d} | {context(b['text'], m.start(), m.end(), 50)}")
    counts["acronyms"] = len(problems)
    out.append(f"## 4. Acronyms used before or without a definition (heuristic): {len(problems)}")
    out.append("Variable names in code font (e.g. BROWNWASH) also show up here; whitelist them with --allow if the paper defines them in words.")
    out.extend(problems)
    out.append("")

    # 6 abstract statistics (user rule S1-56) and 7 define-before-use (S1-115)
    abs_blk = next((b for b in blocks if re.match(r"^\s*abstract\b", b["text"], re.I) and len(b["text"].split()) > 40), None)
    ahits = re.findall(r"\bp\s*[<=>]\s*0?\.\d+|95% CI|\bCI\b|\bt\s*=\s*-?\d|interaction [-+]?\d", abs_blk["text"]) if abs_blk else []
    counts["abstract_stats"] = len(ahits)
    out.append(f"## 6. Statistics in the abstract (p-values, CIs, test statistics): {len(ahits)}")
    out.extend(f"- {h}" for h in ahits)
    out.append("")
    eqpos = {}
    for k, b in enumerate(blocks):
        m = re.search(r"\((\d+)\)\s*$", b["text"])
        if m and ("=" in b["text"] or len(b["text"].split()) <= 3 or b.get("math")):  # a displayed, numbered equation
            eqpos.setdefault(int(m.group(1)), k)
    fwd = []
    first_eq = min(eqpos.values()) if eqpos else None
    for k, b in enumerate(blocks):
        if re.match(r"^\s*references\s*$", b["text"], re.I):
            break
        for m in re.finditer(r"equations? \((\d+)\)", b["text"]):
            n = int(m.group(1))
            if n in eqpos and k < eqpos[n] - 1:  # the sentence that introduces a display equation is fine
                fwd.append(f"- equation ({n}) before it is displayed | {where(b)} | ...{b['text'][max(0, m.start()-60):m.end()+30]}...")
        if first_eq is not None and k < first_eq:
            for sym in re.findall(r"[πβγδθλ]\d", b["text"]):
                fwd.append(f"- symbol {sym} before any equation | {where(b)} | {b['text'][:120]}")
    counts["define_before_use"] = len(fwd)
    out.append(f"## 7. Used before defined (forward equation references, early coefficient symbols): {len(fwd)}")
    out.extend(fwd)
    out.append("")

    # 8 number density in prose (S1-61: narrative results, about three numbers per paragraph)
    dense = []
    for b in prose:
        if re.match(r"^\s*(notes?|source)\s*[:.]", b["text"], re.I):
            continue
        k = len(re.findall(r"(?<![\w(])-?\d+\.\d+", b["text"]))
        if k > 6:
            dense.append(f"- {k} decimals | {where(b)} | {b['text'][:140]}")
    counts["dense_paragraphs"] = len(dense)
    out.append(f"## 8. Number-dense paragraphs (more than 6 decimals; rewrite as narrative): {len(dense)}")
    out.extend(dense)
    out.append("")

    # 9 citation reuse (S1-60: empirical papers from the review come back in results/discussion; theory and method papers may appear once)
    cites, sec = {}, "front"
    pat = re.compile(r"([A-Z][A-Za-z'\-]+)(?: et al\.| (?:and|&) [A-Z][A-Za-z'\-]+)?,? \(?((?:19|20)\d\d)[a-z]?\)?")
    for b in blocks:
        if b["kind"] == "p" and is_heading(b):
            sec = b["text"].strip()[:40]
            continue
        if b["kind"] not in ("p", "footnote"):
            continue
        for m in pat.finditer(b["text"]):
            if m.group(1) in ("Table", "Figure", "Section", "Appendix", "In", "Since", "From", "By", "The", "Until", "After", "Before", "FY", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"):
                continue
            cites.setdefault(f"{m.group(1)} {m.group(2)}", []).append(sec)
    late = re.compile(r"^\s*([4-9]|results|discussion|conclu|robust)", re.I)
    once = sorted(k for k, v in cites.items() if not any(late.match(x) for x in v))
    counts["lit_not_revisited"] = len(once)
    out.append(f"## 9. Citations never revisited in results, discussion or conclusion: {len(once)} of {len(cites)} cited works")
    out.append("Empirical papers from the review should return where the findings are compared (S1-60); theory and method citations have no count requirement. Classify each by hand.")
    for k in once:
        out.append(f"- {k} | {len(cites[k])}x | " + "; ".join(sorted(set(cites[k]))))
    out.append("")

    # 5 note length
    nhits = []
    for b in blocks:
        if re.match(r"^\s*notes?\s*[:.]", b["text"], re.I):
            n = len(sentences(b["text"])); w = len(b["text"].split())
            if n > args.max_note_sentences or w > args.max_note_words or re.search(r"\.\s*\.$", b["text"].strip()):
                nhits.append((f"{n} sentences, {w} words", b))
    counts["long_notes"] = len(nhits)
    out.append(f"## 5. Table/figure notes longer than {args.max_note_sentences} sentences or {args.max_note_words} words (or ending in '. .'): {len(nhits)}")
    for n, b in nhits:
        out.append(f"- {n} | {where(b)} | {b['text'][:220]}")
    out.append("")

    out.insert(2, "Summary: " + ", ".join(f"{k}={v}" for k, v in counts.items()))
    out.insert(3, "")
    report = "\n".join(out)
    print(report)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(report + "\n")
    em = sum(1 for k, _, _ in dash_hits if k == "em dash")
    return 1 if (em or hits) else 0


if __name__ == "__main__":
    sys.exit(main())
