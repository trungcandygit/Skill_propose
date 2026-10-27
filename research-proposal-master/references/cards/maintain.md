# Maintainer card: how to update this skill safely

Load when the user asks to add rules, pull in another skill, change a card, or fix a miss ("cập nhật skill", "thêm rule", "kéo skill về"). Rule IDs are `M-xx`. The long-form guidance is `skills/skill-creator/SKILL.md` (Anthropic, Apache-2.0); this card adapts it to the card/tier design of this skill.

## A. Structure (progressive disclosure)

- **M-01** Keep three levels: frontmatter (name + description, always in context), SKILL.md body (under ~500 lines: card map, loading contract, spine), and resources loaded on demand (cards, references, scripts, source skills). New detail goes into a card or a reference, never into the SKILL.md body. → `skills/skill-creator/SKILL.md#progressive-disclosure`
- **M-02** The description is the trigger: it names what the skill does and the phrases users actually type (Vietnamese and English: "viết đề cương", "đề cương nghiên cứu sinh", "research proposal", "sửa bài theo comment"...). Update it whenever a new use case is added. → `skills/skill-creator/SKILL.md#description-optimization`
- **M-03** One rule per line: ID, rule, why, `→` pointer to the full source. IDs are stable; never renumber; retired rules are marked "(retired YYYY-MM-DD: reason)" instead of deleted.
- **M-04** Every card ends with a `<!-- CARD-END name vN -->` sentinel; bump N when the card changes and update the sentinels quoted in SKILL.md, LOAD.md, PANEL_PROMPTS.md and the hook if it checks them.
- **M-05** Write instructions in the imperative and explain the why; reserve ALWAYS/NEVER for integrity rules. → `skills/skill-creator/SKILL.md#how-to-think-about-improvements`

## B. Adding a source skill (Tier 2)

- **M-10** Gate 0 before copying anything: read the whole SKILL.md and every script; record repo@commit, stars, licence (read the LICENSE file; "no LICENSE" is recorded as such), network calls, and the decision with reason in `references/sources.md`. Skills that send user content to external services are not added. Scripts are never run before they are read.
- **M-11** Copy the source skill unchanged into `skills/<name>/` with a first-line comment naming origin and commit; local restrictions go in the card, not in the copied file.
- **M-12** Distil only actionable rules into a card (one line each, with pointer); do not paste the source. When a new rule conflicts with an existing one, record which wins and why (core C-50).
- **M-13** After adding or changing rules, run `python3 scripts/coverage_check.py --check-pointers` and fix every broken pointer.

## C. Learning from misses

- **M-20** After each panel round or each real use, compare what was missed with what the cards cover; add or restore the rule, and log date, miss and fix in `references/cards/VALIDATION.md` (core C-70).
- **M-21** Generalise from the example: write the rule for the class of error, keep the concrete case as a labelled example, avoid overfitting to one document. → `skills/skill-creator/SKILL.md#how-to-think-about-improvements`
- **M-22** Test changes: keep 2–3 realistic prompts in `evals/evals.json` (e.g. "viết đề cương NCS từ ý tưởng X", "sửa đề cương theo góp ý hội đồng", "kiểm tra đề cương trước khi nộp"); run them with and without the change and compare outputs before merging. → `skills/skill-creator/SKILL.md#running-and-evaluating-test-cases`
- **M-23** Keep the skill lean: remove rules that never fire or that duplicate another rule; read transcripts, not only outputs, to see where the skill wastes effort.

## D. Release

- **M-30** Commit with a message listing cards changed (with new versions), skills added (with licence) and why; update README.md snapshot date. Never commit secrets; check repository visibility before adding personal documents.

## E. Test-first editing (obra writing-skills)

- **M-40** No rule change without a failing case first: run the task without the change, record the exact failure or rationalisation, write the smallest rule that targets it, rerun, then close new loopholes. → `skills/writing-skills/SKILL.md`
- **M-41** Pick the form by failure type: violations under pressure → a prohibition plus a table of rationalisations and red flags; wrong output shape → a recipe naming the parts and their order; a missing element → a REQUIRED slot in the template; condition-dependent behaviour → a conditional on an observable condition. Avoid "unless…" clauses inside rules. → `skills/writing-skills/SKILL.md`
- **M-42** The description states only when to use the skill ("Use when…" plus trigger phrases), not a summary of the workflow, and stays under 1024 characters; agents follow a workflow summary instead of reading the body. → `skills/writing-skills/SKILL.md`; `skills/skill-creator/SKILL.md#description-optimization`
- **M-43** When updating an existing skill keep its name and folder, snapshot the old version as the baseline, and compare with-skill and baseline runs before merging. → `skills/skill-creator/SKILL.md`

<!-- CARD-END maintain v2 -->
