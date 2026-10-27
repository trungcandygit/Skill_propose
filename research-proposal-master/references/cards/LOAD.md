# LOAD block (paste at the top of every agent prompt)

Why: the cards are the complete compressed rule set; an agent that skips one leaves its rules unchecked, and the sentinels prove it read to the end. Pick the block for the seat, paste it verbatim, then add the files and jobs. For full Seat 1 / Seat 2 prompts with every job and placeholder, use `references/cards/PANEL_PROMPTS.md` (it already starts with this block).

## Seat 1 (referee + editor)
```
LOAD FIRST, before any other work (hook-enforced): call Skill("research-proposal-master"), then Read IN FULL (no offset/limit):
  ~/.claude/skills/research-proposal-master/SKILL.md
  ~/.claude/skills/research-proposal-master/references/cards/core.md
  ~/.claude/skills/research-proposal-master/references/cards/seat1-referee-editor.md
  ~/.claude/skills/research-proposal-master/references/cards/proposal.md
  ~/.claude/skills/research-proposal-master/references/cards/deep-search.md
Open a rule's → source under ~/.claude/skills/research-proposal-master/ only when a case needs the detail.
Depth (core C-60 to C-62): read every document in full, recompute every number you verify, no sampling; what you cannot check is UNVERIFIED.
Report line 1: "Loaded: SKILL.md (<n> lines); core.md (<n> lines, <!-- CARD-END core v2 -->); seat1-referee-editor.md (<n> lines, <!-- CARD-END seat1 v1 -->); proposal.md (<n> lines, <!-- CARD-END proposal v2 -->); deep-search.md (<n> lines, <!-- CARD-END deep-search v1 -->)".
Cite rule IDs in every finding (ID | verdict | severity | evidence | fix). Last lines: "rules checked: n/total" for core and for seat1.
```

## Seat 2 (methods + integrity + tables/figures)
```
LOAD FIRST, before any other work (hook-enforced): call Skill("research-proposal-master"), then Read IN FULL (no offset/limit):
  ~/.claude/skills/research-proposal-master/SKILL.md
  ~/.claude/skills/research-proposal-master/references/cards/core.md
  ~/.claude/skills/research-proposal-master/references/cards/seat2-methods-integrity.md
  ~/.claude/skills/research-proposal-master/references/cards/tables-figures.md
  ~/.claude/skills/research-proposal-master/references/cards/proposal.md
  ~/.claude/skills/research-proposal-master/references/cards/deep-search.md
Open a rule's → source under ~/.claude/skills/research-proposal-master/ only when a case needs the detail.
Depth (core C-60 to C-62): rerun the scripts in a scratch copy and diff outputs, recompute every number, render every table and figure page, audit coding year by year (C-65 to C-68); no sampling; what you cannot check is UNVERIFIED.
Report line 1: "Loaded: SKILL.md (<n> lines); core.md (<n> lines, <!-- CARD-END core v2 -->); seat2-methods-integrity.md (<n> lines, <!-- CARD-END seat2 v1 -->); tables-figures.md (<n> lines, <!-- CARD-END tables-figures v1 -->); proposal.md (<n> lines, <!-- CARD-END proposal v2 -->); deep-search.md (<n> lines, <!-- CARD-END deep-search v1 -->)".
Cite rule IDs in every finding (ID | verdict | severity | evidence | fix). Last lines: "rules checked: n/total" for core, seat2 and tables-figures.
```

## Main session (orchestrator)
Read in full: SKILL.md, `references/cards/core.md`, `references/cards/orchestrator.md`; add `seat1-referee-editor.md` before editing prose or the letter, and `seat2-methods-integrity.md` + `tables-figures.md` before R, numbers, tables or figures.

If a card's version changes, update the sentinels quoted above (current: core v2, seat1 v1, seat2 v1, tables-figures v1, orchestrator v1).
