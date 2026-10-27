# Loading manifest

Why this file changed: the old manifest made every agent read 400-600 KB (100-150k tokens) of source skills before working. The rules in those sources are now distilled into cards (one line per rule, stable IDs, a reason, and a pointer back to the source), and `scripts/coverage_check.py` measures how many of the sources' rule sentences the cards cover (target ≥ 90% per role; deliberate omissions are listed with reasons in `cards/coverage-exclusions.md`). Loading got cheaper; the work did not (core C-60 to C-62).

## Tiers

| Tier | Files | Loaded | Size (≈ tokens) |
|---|---|---|---|
| 0 | `SKILL.md`, `cards/core.md` | always, by every role | ≈ 3.8k + 3.8k |
| 1 | `cards/orchestrator.md`, `cards/seat1-referee-editor.md`, `cards/seat2-methods-integrity.md`, `cards/tables-figures.md` | the card(s) of your role, in full | 4.3k / 9.2k / 6.8k / 4.9k |
| 2 | everything under `skills/` and the digests in `references/` | only when a rule's `→` pointer is needed or the case is unusual | 400-600 KB per role if read in full |

## Per-role loading

| Role | Must read in full | Total (≈ tokens) |
|---|---|---|
| Main session (orchestrator) | SKILL.md, core.md, orchestrator.md; plus the Seat 1 card before prose/letter work and the Seat 2 + tables-figures cards before R/numbers/exhibit work | ≈ 12k (up to ≈ 33k when it does all phases itself) |
| Seat 1 agent (referee + editor) | SKILL.md, core.md, seat1-referee-editor.md | ≈ 17k |
| Seat 2 agent (methods + integrity + tables/figures) | SKILL.md, core.md, seat2-methods-integrity.md, tables-figures.md | ≈ 19k |

Proof of loading: the report's first line quotes each card's line count and its `CARD-END` sentinel (see `cards/LOAD.md`). Rule of thumb for Tier 2: open the pointer when you are about to rule FAIL or PASS on a case the card line does not settle, or when you need a template, code, or a threshold table.

## Maintaining the cards

1. After each panel round, log misses in `cards/VALIDATION.md` and add or restore the rule (core C-70).
2. After any card edit, run `python3 scripts/coverage_check.py --check-pointers` and then `python3 scripts/coverage_check.py`; keep every role at ≥ 90%.
3. The role source lists below are what the coverage check reads: each `### ... [role: NAME]` heading lists one role's required sources.


## Tier 2 source lists

### Orchestrator required sources [role: orchestrator]

- `skills/academic-pipeline/SKILL.md`, `skills/academic-pipeline/references/claim_verification_protocol.md`, `skills/academic-pipeline/references/integrity_review_protocol.md`, `skills/academic-pipeline/references/two_stage_review_protocol.md`, `skills/academic-pipeline/references/ai_research_failure_modes.md`, `skills/academic-pipeline/references/reproducibility_audit.md`, `skills/academic-pipeline/references/external_review_protocol.md`, `skills/academic-pipeline/references/claim_audit_calibration_protocol.md`, `skills/academic-pipeline/references/process_summary_protocol.md`, `skills/academic-pipeline/references/plagiarism_detection_protocol.md`, `skills/academic-pipeline/references/score_trajectory_protocol.md`, `skills/academic-pipeline/references/pipeline_state_machine.md`, `skills/academic-pipeline/references/mode_advisor.md`, `skills/academic-pipeline/references/team_collaboration_protocol.md`, `skills/academic-pipeline/references/passport_as_reset_boundary.md`, `skills/academic-pipeline/references/literature_corpus_consumers.md`, `skills/academic-pipeline/references/reinforcement_content.md`, `skills/academic-pipeline/references/progress_dashboard_template.md`
- `references/panel-protocol.md`

#### SEAT 1, group A: referee, response letter, proofreading, style
### A1. Seat 1 required sources [role: seat1]

Directly needed to audit a response letter and revised prose.

- **review-response** (66 KB): `skills/review-response/SKILL.md`, `skills/review-response/references/rebuttal-templates.md`, `skills/review-response/references/response-strategies.md`, `skills/review-response/references/review-classification.md`, `skills/review-response/references/successful-cases.md`, `skills/review-response/references/tone-guidelines.md`
- **nature-response** (40 KB): `skills/nature-response/SKILL.md`, `skills/nature-response/references/action-mapping.md`, `skills/nature-response/references/chinese-author-alignment.md`, `skills/nature-response/references/comment-taxonomy.md`, `skills/nature-response/references/difficult-cases.md`, `skills/nature-response/references/intake-and-routing.md`, `skills/nature-response/references/qa-checklist.md`, `skills/nature-response/references/response-structure.md`, `skills/nature-response/references/source-basis.md`, `skills/nature-response/references/tone-and-stance.md`
- **aer-rebuttal** (21 KB): `skills/aer-rebuttal/SKILL.md`, `skills/aer-rebuttal/references/response-letter-patterns.md`
- **aer-referee-sim** (20 KB): `skills/aer-referee-sim/SKILL.md`, `skills/aer-referee-sim/references/scoring-rubric.md`
- **referee-response** (5 KB): `skills/referee-response/SKILL.md`
- **rebuttal-writing** (7 KB): `skills/rebuttal-writing/SKILL.md`, `skills/rebuttal-writing/references/rebuttal-prompts.md`
- **paper-referee-revise** (28 KB): `skills/paper-referee-revise/SKILL.md`
- **paper-self-revise** (14 KB): `skills/paper-self-revise/SKILL.md`
- **referee-report** (12 KB): `skills/referee-report/SKILL.md`
- **paper-self-review** (6 KB): `skills/paper-self-review/SKILL.md`, `skills/paper-self-review/references/FINAL-VERDICT.md`, `skills/paper-self-review/references/SECTION-CHECKLIST.md`
- **proofreading** (54 KB): `skills/proofreading/SKILL.md`
- **paper-polish** (29 KB): `skills/paper-polish/SKILL.md`
- **academic-proofreader** (12 KB): `skills/academic-proofreader/SKILL.md`
- **stop-slop** (12 KB): `skills/stop-slop/SKILL.md`, `skills/stop-slop/references/examples.md`, `skills/stop-slop/references/phrases.md`, `skills/stop-slop/references/structures.md`
- **econ-write** (54 KB): `skills/econ-write/SKILL.md`

- Digests: `references/revision.md`, `references/response-letter.md`, `references/finance-english-and-machine-checks.md`

Subtotal: about 387 KB (about 96k tokens) plus the digests.

### A2. Seat 1 optional sources (read when the topic is touched)

Nature-family writing and topic-framing material, medical humanizer.

- **humanizer_academic** (51 KB): `skills/humanizer_academic/SKILL.md`
- **master-academic-paper-skill** (42 KB): `skills/master-academic-paper-skill/SKILL.md`, `skills/master-academic-paper-skill/rules/01_master_editorial_philosophy.md`, `skills/master-academic-paper-skill/rules/02_mechanical_and_anti_ai_gate.md`, `skills/master-academic-paper-skill/rules/03_semantic_and_logic_gate.md`, `skills/master-academic-paper-skill/rules/05_latex_tables_and_math_notation.md`, `skills/master-academic-paper-skill/rules/06_figure_synthesis_and_visuals.md`
- **nature-polishing** (43 KB): `skills/nature-polishing/SKILL.md`, `skills/nature-polishing/references/latex-layout.md`, `skills/nature-polishing/references/nat-comms-2025-diction.md`, `skills/nature-polishing/references/phrasebank-playbook.md`, `skills/nature-polishing/references/published-article-patterns.md`, `skills/nature-polishing/references/section-moves.md`, `skills/nature-polishing/references/style-guardrails.md`, `skills/nature-polishing/references/writing-strategy.md`
- **nature-social-science** (236 KB): `skills/nature-social-science/SKILL.md`, `skills/nature-social-science/references/01-foundations.md`, `skills/nature-social-science/references/02-workflow-steps1-3.md`, `skills/nature-social-science/references/03-workflow-steps4-5.md`, `skills/nature-social-science/references/04-workflow-steps6-8.md`, `skills/nature-social-science/references/05-prompt-library.md`, `skills/nature-social-science/references/06-worksheets.md`, `skills/nature-social-science/references/07-status-terminology.md`, `skills/nature-social-science/references/08-usage-handoff.md`, `skills/nature-social-science/references/09-academic-expression.md`
- **nature-reviewer** (77 KB): `skills/nature-reviewer/SKILL.md`, `skills/nature-reviewer/references/domain-specific-review-gates.md`, `skills/nature-reviewer/references/editorial criteria and processes.md`, `skills/nature-reviewer/references/forensic-consistency-audit.md`, `skills/nature-reviewer/references/qa-checklist.md`, `skills/nature-reviewer/references/report-structure.md`, `skills/nature-reviewer/references/review-axes.md`, `skills/nature-reviewer/references/reviewer-workflow.md`, `skills/nature-reviewer/references/role-boundaries.md`, `skills/nature-reviewer/references/source-basis.md`, `skills/nature-reviewer/references/technical-concern-taxonomy.md`
- **nature-writing** (135 KB): `skills/nature-writing/SKILL.md`, `skills/nature-writing/references/abstract.md`, `skills/nature-writing/references/article-architecture.md`, `skills/nature-writing/references/chinese-author-workflow.md`, `skills/nature-writing/references/conclusion.md`, `skills/nature-writing/references/examples/abstract-examples.md`, `skills/nature-writing/references/examples/abstract/template-a.md`, `skills/nature-writing/references/examples/abstract/template-b.md`, `skills/nature-writing/references/examples/abstract/template-c.md`, `skills/nature-writing/references/examples/index.md`, `skills/nature-writing/references/examples/introduction-examples.md`, `skills/nature-writing/references/examples/introduction/novel-task-challenge-decomposition.md`, `skills/nature-writing/references/examples/introduction/pipeline-not-recommended-abstract-only.md`, `skills/nature-writing/references/examples/introduction/pipeline-version-1-one-contribution-multi-advantages.md`, `skills/nature-writing/references/examples/introduction/pipeline-version-2-two-contributions.md`, `skills/nature-writing/references/examples/introduction/pipeline-version-3-new-module-on-existing-pipeline.md`, `skills/nature-writing/references/examples/introduction/pipeline-version-4-observation-driven.md`, `skills/nature-writing/references/examples/introduction/technical-challenge-version-1-existing-task.md`, `skills/nature-writing/references/examples/introduction/technical-challenge-version-2-existing-task-insight-backed-by-traditional.md`, `skills/nature-writing/references/examples/introduction/technical-challenge-version-3-novel-task.md`, `skills/nature-writing/references/examples/introduction/version-1-task-then-application.md`, `skills/nature-writing/references/examples/introduction/version-2-application-first.md`, `skills/nature-writing/references/examples/introduction/version-3-general-to-specific-setting.md`, `skills/nature-writing/references/examples/introduction/version-4-open-with-challenge.md`, `skills/nature-writing/references/examples/method-examples.md`, `skills/nature-writing/references/examples/method/example-of-the-three-elements.md`, `skills/nature-writing/references/examples/method/method-writing-common-issues-note.md`, `skills/nature-writing/references/examples/method/module-design-instant-ngp.md`, `skills/nature-writing/references/examples/method/module-motivation-patterns.md`, `skills/nature-writing/references/examples/method/module-triad-neural-body.md`, `skills/nature-writing/references/examples/method/neural-body-annotated-figure-text.md`, `skills/nature-writing/references/examples/method/overview-template.md`, `skills/nature-writing/references/examples/method/pre-writing-questions.md`, `skills/nature-writing/references/examples/method/section-skeleton.md`, `skills/nature-writing/references/experiments.md`, `skills/nature-writing/references/introduction.md`, `skills/nature-writing/references/method.md`, `skills/nature-writing/references/nat-comms-2025-corpus.md`, `skills/nature-writing/references/nature-summary-paragraph.md`, `skills/nature-writing/references/paper-review.md`, `skills/nature-writing/references/paragraph-flow.md`, `skills/nature-writing/references/related-work.md`, `skills/nature-writing/references/submission-package.md`

Subtotal: about 587 KB (about 146k tokens).

#### SEAT 2, group B: methods, reproduction, tables, figures, citations
### B1. Seat 2 required sources [role: seat2]

Directly needed to audit numbers, designs, tables, figures, and citations.

- **aer-consistency** (19 KB): `skills/aer-consistency/SKILL.md`, `skills/aer-consistency/references/audit-checklist.md`
- **audit-reproducibility** (42 KB): `skills/audit-reproducibility/SKILL.md`, `skills/audit-reproducibility/rules/replication-protocol.md`
- **audit-replication** (3 KB): `skills/audit-replication/SKILL.md`
- **aer-identification** (29 KB): `skills/aer-identification/SKILL.md`, `skills/aer-identification/references/estimator-playbook.md`
- **aer-robustness** (22 KB): `skills/aer-robustness/SKILL.md`, `skills/aer-robustness/references/robustness-menu.md`
- **did-analysis** (14 KB): `skills/did-analysis/SKILL.md`, `skills/did-analysis/references/did-reference.md`
- **iv-estimation** (15 KB): `skills/iv-estimation/SKILL.md`, `skills/iv-estimation/references/iv-reference.md`
- **panel-data** (14 KB): `skills/panel-data/SKILL.md`, `skills/panel-data/references/panel-reference.md`
- **phack-detection** (9 KB): `skills/phack-detection/SKILL.md`
- **specification-search** (13 KB): `skills/specification-search/SKILL.md`
- **econ-robustness-checks** (6 KB): `skills/econ-robustness-checks/SKILL.md`
- **aer-tables-figures** (17 KB): `skills/aer-tables-figures/SKILL.md`, `skills/aer-tables-figures/references/exhibit-cookbook.md`
- **econ-table** (13 KB): `skills/econ-table/SKILL.md`
- **econ-figure** (23 KB): `skills/econ-figure/SKILL.md`
- **econ-stats** (8 KB): `skills/econ-stats/SKILL.md`
- **ggplot2** (8 KB): `skills/ggplot2/SKILL.md`
- **scientific-visualization** (71 KB): `skills/scientific-visualization/SKILL.md`, `skills/scientific-visualization/references/color_palettes.md`, `skills/scientific-visualization/references/journal_requirements.md`, `skills/scientific-visualization/references/matplotlib_examples.md`, `skills/scientific-visualization/references/publication_guidelines.md`, `skills/scientific-visualization/references/sources.md`
- **reference-verify** (25 KB): `skills/reference-verify/SKILL.md`
- **citation-verification** (34 KB): `skills/citation-verification/SKILL.md`, `skills/citation-verification/references/api-usage.md`, `skills/citation-verification/references/common-errors.md`, `skills/citation-verification/references/verification-rules.md`
- **nature-statistics** (30 KB): `skills/nature-statistics/SKILL.md`, `skills/nature-statistics/references/common-failure-modes.md`, `skills/nature-statistics/references/figure-statistics.md`, `skills/nature-statistics/references/nature-article-requirements.md`, `skills/nature-statistics/references/reviewer-checklist.md`, `skills/nature-statistics/references/source-basis.md`, `skills/nature-statistics/references/statistical-reporting.md`

- Figure sources for the tables-figures card: `skills/nature-figure/SKILL.md`, `skills/nature-figure/references/figure-contract.md`, `skills/nature-figure/references/figure-legend-conventions.md`, `skills/nature-figure/references/nature-article-requirements.md`, `skills/nature-figure/references/qa-contract.md`, `skills/nature-figure/references/multipanel-evidence-architecture.md`
- Digests: `references/r-data.md`, `references/methods-gap-fill.md`

Subtotal: about 424 KB (about 106k tokens) plus the figure sources and digests.

### B2. Seat 2 optional sources (read when the topic is touched)

Full R pipeline, other designs, Nature figure gallery, R style.

- **empirical-analysis-r** (237 KB): `skills/empirical-analysis-r/SKILL.md`, `skills/empirical-analysis-r/references/01-data-cleaning.md`, `skills/empirical-analysis-r/references/02-data-transformation.md`, `skills/empirical-analysis-r/references/03-descriptive-stats.md`, `skills/empirical-analysis-r/references/04-statistical-tests.md`, `skills/empirical-analysis-r/references/05-modeling.md`, `skills/empirical-analysis-r/references/06-robustness.md`, `skills/empirical-analysis-r/references/07-further-analysis.md`, `skills/empirical-analysis-r/references/08-tables-plots.md`
- **econ-causal-inference-guide** (6 KB): `skills/econ-causal-inference-guide/SKILL.md`
- **ols-regression** (10 KB): `skills/ols-regression/SKILL.md`, `skills/ols-regression/references/ols-reference.md`
- **time-series** (12 KB): `skills/time-series/SKILL.md`, `skills/time-series/references/time-series-reference.md`
- **synthetic-control** (21 KB): `skills/synthetic-control/SKILL.md`, `skills/synthetic-control/references/synthetic-control-reference.md`
- **rdd-analysis** (14 KB): `skills/rdd-analysis/SKILL.md`, `skills/rdd-analysis/references/rdd-reference.md`
- **marginaleffects** (8 KB): `skills/marginaleffects/SKILL.md`
- **nature-figure** (198 KB): `skills/nature-figure/SKILL.md`, `skills/nature-figure/references/ai-graphical-abstract-workflow.md`, `skills/nature-figure/references/api.md`, `skills/nature-figure/references/asset-adaptation.md`, `skills/nature-figure/references/backend-selection.md`, `skills/nature-figure/references/chart-types.md`, `skills/nature-figure/references/common-patterns.md`, `skills/nature-figure/references/demos.md`, `skills/nature-figure/references/design-theory.md`, `skills/nature-figure/references/figure-contract.md`, `skills/nature-figure/references/figure-legend-conventions.md`, `skills/nature-figure/references/multipanel-evidence-architecture.md`, `skills/nature-figure/references/nature-2026-observations.md`, `skills/nature-figure/references/nature-article-requirements.md`, `skills/nature-figure/references/openrouter-image-generation.md`, `skills/nature-figure/references/qa-contract.md`, `skills/nature-figure/references/r-template-index.md`, `skills/nature-figure/references/r-workflow.md`, `skills/nature-figure/references/template-catalog.md`, `skills/nature-figure/references/tutorials.md`, `skills/nature-figure/references/vector-schematic-style-rules.md`, `skills/nature-figure/references/vector-schematic-workflow.md`
- **tidyverse-patterns** (11 KB): `skills/tidyverse-patterns/SKILL.md`
- **r-style-guide** (6 KB): `skills/r-style-guide/SKILL.md`

Subtotal: about 529 KB (about 132k tokens).
