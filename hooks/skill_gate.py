#!/usr/bin/env python3
"""Force-load gate for the academic skills.

  skill_gate.py mark   PostToolUse(Skill|Read): record that a required skill was invoked, or that a
                       research-proposal-master card was read in full (no offset/limit), in this session/agent.
  skill_gate.py check  PreToolUse(Write|Edit|NotebookEdit|Agent|Artifact): deny until everything is loaded.
Scope of the gate: only when cwd or target path is under an NCKH folder.
Requirements (each agent keyed separately when the hook input carries agent_id):
  1. Skill("academic-pipeline") and Skill("research-proposal-master") invoked;
  2. once the compressed tiers exist: references/cards/core.md read in full plus at least one role card.
"""
import json, os, sys

STATE = os.path.expanduser("~/.claude/state/skills_loaded")
CARDS = os.path.expanduser("~/.claude/skills/research-proposal-master/references/cards")
SKILLS = ("academic-pipeline", "research-proposal-master")
ROLE_CARDS = ("seat1-referee-editor.md", "seat2-methods-integrity.md", "tables-figures.md", "orchestrator.md", "proposal.md", "deep-search.md")


def key(d):
    return (d.get("session_id") or "unknown") + ("." + d["agent_id"] if d.get("agent_id") else "")


def marks(k):
    p = os.path.join(STATE, k)
    try:
        return set(open(p).read().split())
    except OSError:
        return set()


def add(k, item):
    os.makedirs(STATE, exist_ok=True)
    m = marks(k) | {item}
    open(os.path.join(STATE, k), "w").write("\n".join(sorted(m)))


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"
    d = json.load(sys.stdin)
    k = key(d)
    ti = d.get("tool_input") or {}
    if mode == "mark":
        name = str(ti.get("skill", "")).split(":")[-1]
        if name in SKILLS:
            add(k, "skill:" + name)
        fp = str(ti.get("file_path", ""))
        if fp.startswith(CARDS) and not ti.get("offset") and not ti.get("limit"):
            add(k, "card:" + os.path.basename(fp))
        return
    scope = " ".join([d.get("cwd", ""), str(ti.get("file_path", "")), str(ti.get("path", ""))])
    m = marks(k)
    if d.get("agent_id"):  # subagent inherits nothing it did not load itself, except the parent's Skill calls
        m |= {x for x in marks(d.get("session_id") or "unknown") if x.startswith("skill:")}
    in_nckh = "NCKH" in scope
    # Any project: once research-proposal-master is in use, its cards must be loaded before writing or spawning.
    if not in_nckh and "skill:research-proposal-master" not in m:
        return
    missing = [f'Skill("{s}")' for s in SKILLS if "skill:" + s not in m] if in_nckh else []
    if os.path.exists(os.path.join(CARDS, "core.md")):
        if "card:core.md" not in m:
            missing.append(f"Read {CARDS}/core.md (whole file, no offset/limit)")
        present = [c for c in ROLE_CARDS if os.path.exists(os.path.join(CARDS, c))]
        if present and not any("card:" + c in m for c in present):
            missing.append(f"Read your role card(s) in full from {CARDS}/ (" + ", ".join(ROLE_CARDS) + ")")
    if not missing:
        return
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": (
            "BLOCKED (user rule: load the full compressed skill before any academic task). Missing: "
            + "; ".join(missing) + ". Do these, then retry. See references/cards/LOAD.md."
        )}}))


main()
