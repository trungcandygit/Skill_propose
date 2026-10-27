#!/usr/bin/env python3
"""Measure how well the rule cards cover the rule-like sentences in their sources.

Why this exists: the cards in references/cards/ are a compressed stand-in for
~800 KB of bundled source skills. Compression is only safe if we can show that
the rules in the sources survive in the cards. This script extracts every
rule-like sentence (one containing must, never, always, do not, don't,
required, IRON RULE, should, avoid) from each role's required source files,
scores it against every card rule the role loads, and reports coverage plus
the sentences no card rule covers.

How roles are defined: `references/full-read-manifest.md`, section
"Tier 2 source lists", has one `###` heading per role tagged `[role: NAME]`;
every backticked path below that heading is a required source. Paths are
relative to the skill folder (or start with ~). Which cards a role loads is
set in ROLE_CARDS below and must match SKILL.md.

Matching: a source sentence is reduced to content tokens (lower-cased, crude
stemming, stop words dropped). For each card rule we compute
containment = |sentence tokens found in rule| / |sentence tokens| and a
difflib ratio; the score is the larger of the two. A sentence counts as
covered when its best score reaches --threshold (default 0.5).

Exclusions: `references/cards/coverage-exclusions.md`. Each bullet is one of
    - file: `glob` -- reason
    - regex: `pattern` -- reason
    - text: `exact sentence prefix` -- reason
A bullet without a reason is rejected, so every omission stays explained.

Usage:
    python3 scripts/coverage_check.py                # summary for all roles
    python3 scripts/coverage_check.py --role seat1 --show 40
    python3 scripts/coverage_check.py --out /tmp/uncovered.md
    python3 scripts/coverage_check.py --dump-sources seat2 > seat2_rules.txt
    python3 scripts/coverage_check.py --check-pointers

Standard library only. Exit code 1 if any role is below --min (default 90).
"""
import argparse
import difflib
import fnmatch
import math
import os
import re
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARDS_DIR = os.path.join(SKILL_DIR, "references", "cards")
MANIFEST = os.path.join(SKILL_DIR, "references", "full-read-manifest.md")
EXCLUSIONS = os.path.join(CARDS_DIR, "coverage-exclusions.md")

ROLE_CARDS = {
    "orchestrator": ["core.md", "orchestrator.md"],
    "seat1": ["core.md", "seat1-referee-editor.md"],
    "seat2": ["core.md", "seat2-methods-integrity.md", "tables-figures.md"],
}

USE_IDF = False  # set by --idf; plain containment is the default

KEYWORDS = re.compile(
    r"\b(must|never|always|do not|don't|required|iron rule|should|avoid)\b", re.I
)
RULE_LINE = re.compile(r"^\s*[-*]\s*\**\s*([A-Z]{1,5}\d?-\d{2,3})\**")
STOP = set(
    """a an the and or of to in on for with by from as at is are be been being
    it its this that these those which who whom what when where why how not no
    do does did don t must never always should required avoid iron rule rules
    can could may might will would shall into than then there their they them
    we our you your i he she his her if else so such any all each every only
    also more most less very just but about over under per via use used using
    e g eg ie i.e etc one two s x y have has had was were""".split()
)


# Light synonym folding so a faithful paraphrase is not scored as a miss.
SYNONYMS = {
    "fabricat": "invent", "make": "invent", "hallucinat": "invent", "manufactur": "invent",
    "complete": "full", "entire": "full", "whole": "full", "verbatim": "full",
    "trim": "truncat", "abbreviat": "truncat", "shorten": "truncat",
    "referee": "reviewer", "review": "reviewer", "critic": "criticism",
    "manuscript": "paper", "draft": "paper", "articl": "paper",
    "skip": "ignor", "drop": "ignor", "omit": "ignor", "sidestep": "deflect",
    "dismiss": "deflect", "evad": "deflect", "evasive": "deflect",
    "modify": "edit", "chang": "edit", "revis": "edit", "alter": "edit", "rewrit": "edit",
    "cite": "citation", "reference": "citation", "bibliograph": "citation", "bib": "citation",
    "figur": "figure", "fig": "figure", "plot": "figure", "chart": "figure", "graph": "figure",
    "tabl": "table", "exhibit": "table",
    "se": "error", "standard": "error",
    "accusatory": "hostile", "combative": "hostile", "defensiv": "hostile", "sarcastic": "hostile",
    "promis": "promise", "consider": "promise",
    "number": "numer", "value": "numer", "numerical": "numer", "statistic": "numer",
    "result": "finding", "finding": "finding", "estimat": "finding",
    "em": "dash", "emdash": "dash",
    "cluster": "cluster", "clustered": "cluster",
    "causal": "caus", "causality": "caus", "causation": "caus",
    "limitation": "limit", "caveat": "limit", "weakness": "limit",
    "assess": "check", "audit": "check", "verify": "check", "verif": "check", "confirm": "check", "test": "check",
}


def stem(w):
    if w in SYNONYMS:
        return SYNONYMS[w]
    for suf in ("ations", "ation", "ings", "ing", "ies", "ied", "ed", "es", "s", "ly", "al"):
        if len(w) > len(suf) + 3 and w.endswith(suf):
            w = w[: -len(suf)]
            break
    if len(w) > 4 and w[-1] == w[-2] and w[-1] not in "aeiou":
        w = w[:-1]  # trimmed -> trimm -> trim
    if len(w) > 5 and w.endswith("e"):
        w = w[:-1]  # truncate -> truncat
    return SYNONYMS.get(w, w)


def tokens(text):
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {stem(w) for w in words if w not in STOP and len(w) > 1}


def strip_code(text):
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"^---\n.*?\n---\n", " ", text, flags=re.S)  # YAML front matter
    return text


BLOCK_START = re.compile(r"^\s*([#>|]|[-*+]\s|\d+[.)]\s|\[[ x]\])")


def paragraphs(text):
    """Join hard-wrapped lines so a wrapped sentence is not cut into fragments."""
    out, cur = [], []
    for raw in strip_code(text).splitlines():
        line = raw.rstrip()
        if not line.strip() or line.strip().startswith("|---"):
            if cur:
                out.append(" ".join(cur))
                cur = []
            continue
        if BLOCK_START.match(line) and cur:
            out.append(" ".join(cur))
            cur = []
        cur.append(line.strip())
        if line.lstrip().startswith(("#", "|")):
            out.append(" ".join(cur))
            cur = []
    if cur:
        out.append(" ".join(cur))
    return out


def split_sentences(text):
    out = []
    for para in paragraphs(text):
        para = re.sub(r"^[#>*\-+\d.)\s|\[\]x]+", "", para)
        for part in re.split(r"(?<=[.!?])\s+(?=[A-Z\"'(`*])|\s\|\s", para):
            part = part.strip(" |*`")
            if len(part) >= 12:
                out.append(part)
    return out


def rule_sentences(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError:
        return []
    return [s for s in split_sentences(text) if KEYWORDS.search(s)]


def parse_manifest():
    roles = {}
    if not os.path.exists(MANIFEST):
        return roles
    with open(MANIFEST, encoding="utf-8") as fh:
        text = fh.read()
    m = re.search(r"^## Tier 2 source lists.*?$(.*)", text, re.M | re.S)
    if not m:
        return roles
    current = None
    for line in m.group(1).splitlines():
        h = re.match(r"^###.*\[role:\s*(\w[\w-]*)\]", line)
        if h:
            current = h.group(1)
            roles.setdefault(current, [])
            continue
        if line.startswith("#"):
            current = None  # untagged heading (e.g. optional lists) ends the role block
            continue
        if line.startswith("## "):
            break
        if current:
            for p in re.findall(r"`([^`]+\.md)`", line):
                roles[current].append(p)
    return roles


def resolve(p):
    p = os.path.expanduser(p)
    return p if os.path.isabs(p) else os.path.join(SKILL_DIR, p)


def load_exclusions():
    rules = []
    if not os.path.exists(EXCLUSIONS):
        return rules
    pat = re.compile(r"^- (file|regex|text): `(.+?)`\s+(?:--|—|-)\s+(.+)$")
    with open(EXCLUSIONS, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            line = line.rstrip()
            if not re.match(r"^- (file|regex|text):", line):
                continue
            m = pat.match(line)
            if not m or len(m.group(3).strip()) < 4:
                sys.exit(f"coverage-exclusions.md line {n}: missing reason: {line}")
            kind, val, reason = m.groups()
            rules.append((kind, val, reason))
    return rules


def excluded(rel, sentence, rules):
    for kind, val, reason in rules:
        if kind == "file" and fnmatch.fnmatch(rel, val):
            return reason
        if kind == "regex" and re.search(val, sentence, re.I):
            return reason
        if kind == "text" and sentence.startswith(val):
            return reason
    return None


def load_cards(names):
    rules = []
    for name in names:
        path = os.path.join(CARDS_DIR, name)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                m = RULE_LINE.match(line)
                if m:
                    body = re.sub(r"`skills/[^`]*`|`references/[^`]*`", " ", line)
                    rules.append((m.group(1), body.strip(), tokens(body)))
    return rules


def idf_weights(card_rules):
    """Rare words count more: matching 'Hansen' says more than matching 'paper'."""
    n = len(card_rules) or 1
    df = {}
    for _, _, rt in card_rules:
        for t in rt:
            df[t] = df.get(t, 0) + 1
    return lambda t: math.log(1.0 + n / (1.0 + df.get(t, 0)))


def best_match(sentence, card_rules, weight=None):
    st = tokens(sentence)
    if not st:
        return 1.0, None
    weight = weight or (lambda t: 1.0)
    total = sum(weight(t) for t in st)
    best, best_id = 0.0, None
    low = sentence.lower()
    for rid, body, rt in card_rules:
        cont = sum(weight(t) for t in st & rt) / total
        score = cont
        if cont > 0.25:
            score = max(cont, difflib.SequenceMatcher(None, low, body.lower()).ratio())
        if score > best:
            best, best_id = score, rid
    return best, best_id


def role_report(role, sources, threshold, excl):
    card_rules = load_cards(ROLE_CARDS.get(role, ["core.md"]))
    weight = idf_weights(card_rules)
    seen, rows = set(), []
    n_excl = 0
    for rel in sources:
        path = resolve(rel)
        for s in rule_sentences(path):
            key = re.sub(r"\W+", " ", s.lower()).strip()
            if key in seen:
                continue
            seen.add(key)
            if excluded(rel, s, excl):
                n_excl += 1
                continue
            score, rid = best_match(s, card_rules, weight if USE_IDF else None)
            rows.append((rel, s, score, rid))
    covered = [r for r in rows if r[2] >= threshold]
    pct = 100.0 * len(covered) / len(rows) if rows else 100.0
    return {
        "role": role,
        "cards": ROLE_CARDS.get(role),
        "card_rules": len(card_rules),
        "extracted": len(rows) + n_excl,
        "excluded": n_excl,
        "eligible": len(rows),
        "covered": len(covered),
        "pct": pct,
        "uncovered": [r for r in rows if r[2] < threshold],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--role", help="only this role (orchestrator, seat1, seat2)")
    ap.add_argument("--threshold", type=float, default=0.5)
    ap.add_argument("--min", type=float, default=90.0, help="pass mark in percent")
    ap.add_argument("--show", type=int, default=0, help="print N uncovered sentences per role")
    ap.add_argument("--out", help="write all uncovered sentences to this markdown file")
    ap.add_argument("--dump-sources", metavar="ROLE", help="print the extracted rule sentences of ROLE and exit")
    ap.add_argument("--idf", action="store_true", help="weight rare words more (stricter; default is plain containment)")
    ap.add_argument("--check-pointers", action="store_true", help="verify that every card pointer names an existing file")
    args = ap.parse_args()
    global USE_IDF
    USE_IDF = args.idf

    if args.check_pointers:
        bad = 0
        for name in sorted(set(sum(ROLE_CARDS.values(), []))):
            with open(os.path.join(CARDS_DIR, name), encoding="utf-8") as fh:
                for n, line in enumerate(fh, 1):
                    for ptr in re.findall(r"→ `([^`#]+)(?:#[^`]*)?`", line):
                        if ptr.startswith("SKILL.md"):
                            ptr_path = os.path.join(SKILL_DIR, "SKILL.md")
                        else:
                            ptr_path = resolve(ptr)
                        if not os.path.exists(ptr_path):
                            bad += 1
                            print(f"{name}:{n}: missing pointer target {ptr}")
        print(f"pointer check: {bad} missing")
        if bad:
            return 1

    roles = parse_manifest()
    if not roles:
        sys.exit("No '## Tier 2 source lists' with '[role: ...]' headings found in the manifest.")
    excl = load_exclusions()

    if args.dump_sources:
        for rel in roles.get(args.dump_sources, []):
            print(f"\n## {rel}")
            for s in rule_sentences(resolve(rel)):
                print("-", s)
        return 0

    names = [args.role] if args.role else list(roles)
    reports = [role_report(r, roles[r], args.threshold, excl) for r in names]
    failed = False
    out_lines = []
    for rep in reports:
        print(
            f"{rep['role']:13s} cards={'+'.join(rep['cards'] or [])} rules={rep['card_rules']} "
            f"extracted={rep['extracted']} excluded={rep['excluded']} eligible={rep['eligible']} "
            f"covered={rep['covered']} coverage={rep['pct']:.1f}%"
        )
        if rep["pct"] < args.min:
            failed = True
        for rel, s, score, rid in rep["uncovered"][: args.show]:
            print(f"   [{score:.2f} {rid}] {rel}: {s[:200]}")
        out_lines.append(f"\n## {rep['role']} ({rep['pct']:.1f}%)\n")
        for rel, s, score, rid in rep["uncovered"]:
            out_lines.append(f"- [{score:.2f} {rid}] `{rel}`: {s}")
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write("\n".join(out_lines) + "\n")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
