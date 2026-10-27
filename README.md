# research-proposal-master

A super-skill for writing, auditing and revising research proposals (đề cương nghiên cứu sinh, luận án, luận văn, thuyết minh đề tài, grant, pre-analysis plan) in empirical finance, economics and social science. It is built on `paper-revision-master` (trungcandygit/SKILL_ACADEMIC, snapshot 2026-10-23), keeps all of its integrity, causal-wording, identification and panel rules, removes journal-format rules, and adds proposal, deep-search and maintenance cards plus five of the strongest open proposal skills.

## Contents

- `research-proposal-master/SKILL.md`: entry point, card map, loading contract, proposal spine P0–P8.
- `research-proposal-master/references/cards/`
  - `core.md` (Tier 0, always).
  - `proposal.md`: about 75 proposal rules (P-01 to P-104): call and template compliance, eligibility, problem–gap–contribution, aims and hypotheses, design and inference, power/MDE, pre-registration, data plan, feasibility, products, Vietnamese PhD conventions and APA, committee review lens, consistency matrix, outline approval, write-with-verify.
  - `deep-search.md`: precise search of primary sources (law to the article/clause/point, papers to the table/page, data to the series), source hierarchy, search log, document request list for the user.
  - `orchestrator.md`, `seat1-referee-editor.md`, `seat2-methods-integrity.md`, `tables-figures.md`: role cards from the base skill.
  - `maintain.md`: how to update this skill (skill-creator and test-first editing).
  - `LOAD.md`, `PANEL_PROMPTS.md` (two-seat panel with PROPOSAL MODE jobs), `VALIDATION.md`.
- `research-proposal-master/references/sources.md`: provenance and licence of every added skill.
- `research-proposal-master/scripts/`: deterministic checks (style, cross-references, numbers, figures), dossier builder, coverage check, hooks.
- `research-proposal-master/skills/`: about 215 source skills, including research-proposal (luwill), grant-proposal, preregister, power-analysis, interview-me, data-management-plan (pedrohcgs), research-grants (K-Dense), review-pap, proposal-revise, skill-creator (Anthropic), writing-skills (obra).
- `hooks/`: two optional enforcement hooks.

## Install

1. Copy `research-proposal-master/` to `~/.claude/skills/` (or to a project's `.claude/skills/`).
2. Optional: copy `hooks/*.py` to `~/.claude/hooks/` and follow `research-proposal-master/scripts/hooks/INSTALL.md`.
3. Ask, for example: "viết đề cương nghiên cứu sinh về …", "sửa đề cương theo góp ý hội đồng", "kiểm tra đề cương trước khi nộp".

## Licences

Bundled skills keep their own licences (see `references/sources.md` and the base README). Some bundled skills have no LICENSE file; if this repository stays public, review that list.

Snapshot date: 2026-10-27.
