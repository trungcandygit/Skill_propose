#!/usr/bin/env python3
"""UserPromptSubmit hook: inject a digest of the academic skills on every prompt."""
import json, os, re

SK = os.path.expanduser("~/.claude/skills")
SKILLS = ["academic-pipeline", "academic-paper", "stop-slop", "proofreading"]
PER_SKILL = 2200  # chars per skill digest

def digest(name):
    p = os.path.join(SK, name, "SKILL.md")
    try:
        t = open(p, encoding="utf-8").read()
    except OSError:
        return f"[{name}] MISSING: {p}"
    t = re.sub(r"^---.*?---\s*", "", t, flags=re.S)  # drop frontmatter
    keep = []
    for line in t.splitlines():
        s = line.strip()
        if s.startswith("#") or "IRON RULE" in s or re.match(r"^\d+\.\s\*\*", s) or s.startswith("| ") and "Anti-Pattern" not in s and len(keep) < 5:
            keep.append(s)
    out = "\n".join(keep)
    return f"[{name}] full text: {p}\n{out[:PER_SKILL]}"

ctx = (
    "BAT BUOC (yeu cau nguoi dung): moi task hoc thuat phai theo dung skill. "
    "Goi Skill(\"academic-pipeline\") (va Skill(\"academic-paper\"), Skill(\"stop-slop\"), Skill(\"proofreading\") o giai doan tuong ung) "
    "neu chua duoc load trong phien nay; neu Skill tool loi thi Read truc tiep file SKILL.md o duong dan ben duoi. "
    "Lam DU cac stage, khong bo buoc integrity/review. "
    "Skill gop: Skill(\"research-proposal-master\") roi Read TRON VEN (khong offset/limit) references/cards/core.md + the vai tro (orchestrator / seat1-referee-editor / seat2-methods-integrity / tables-figures); "
    "moi prompt agent phai dan khoi trong references/cards/LOAD.md; hook skill_gate chan Write/Edit/Agent trong NCKH neu thieu.\n\n"
    + "\n\n".join(digest(n) for n in SKILLS)
)
print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": ctx}}))
