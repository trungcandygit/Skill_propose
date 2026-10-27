# Coverage exclusions

`scripts/coverage_check.py` skips the source sentences matched below. Every entry needs a reason, so an omission from the cards is always a decision, not an accident. Reasons fall into five kinds: **duplicate** (the rule lives in another role's card), **off-topic** (not used when revising an empirical finance or economics paper), **tooling** (instructions for a bundled script or service this skill does not run; the principle is kept in a card), **house style** (a convention of one source author), **non-rule** (a heading, example or description that only looks like a rule).

Format: `- file|regex|text: `pattern` -- reason`. `file` is a glob on the source path; `regex` is case-insensitive on the sentence; `text` is a sentence prefix.

## Orchestrator sources (academic-pipeline internals)

- file: `skills/academic-pipeline/references/passport_as_reset_boundary.md` -- tooling: ARS session-reset passport, hashes and file locks; this skill never runs that machinery (O-36 keeps the user-decision rule)
- file: `skills/academic-pipeline/references/literature_corpus_consumers.md` -- tooling: ARS literature-corpus contract for deep-research agents, not part of revising a paper
- file: `skills/academic-pipeline/references/claim_audit_calibration_protocol.md` -- tooling: gold-set calibration of the ARS claim-audit judge
- file: `skills/academic-pipeline/references/team_collaboration_protocol.md` -- off-topic: multi-author ARS role assignment and git attribution
- file: `skills/academic-pipeline/references/claim_verification_protocol.md` -- tooling: ARS Phase E evidence-row schema and renderer; principle kept in C-06, O-65
- file: `skills/academic-pipeline/references/two_stage_review_protocol.md` -- tooling: ARS re-review input manifest; principle kept in O-51
- file: `skills/academic-pipeline/references/mode_advisor.md` -- tooling: ARS mode selection menu
- file: `skills/academic-pipeline/references/progress_dashboard_template.md` -- non-rule: dashboard template
- regex: `#\d{3}|Schema \d|input_binding|artifact_sha|manifest|sidecar|passport|ledger binding|audit ledger|run_id|state_tracker|frontmatter` -- tooling: ARS issue numbers, schemas and state files
- regex: `observer|collaboration_depth|LLM-ADVISORY|UNMEASURED|HEURISTIC-ADVISORY|advisory only|ADVISORY ONLY|tortured-phrase|criterion_trajectory|score_trajectory` -- tooling: ARS advisory side channels that never gate a decision
- regex: `\bSLIM\b|awaiting_resume|pending_decision|resume_from|ARS_|sr-screener|single-phase agent|routing core|Routing discipline|Route to that mode|intent_clarification` -- tooling: ARS routing and resume mechanics
- regex: `tier below|Tiers are relative|model ids|prompt cache|same worker|cross-model|averaged across models` -- tooling: ARS model-tiering options
- regex: `Phase E|evidence rows?|E4|SCOPE-BROADENED|STRENGTH-DRIFTED|RANDOM`, `TOP-UP|registry|Eligibility never|probe|legacy-a|E_claims|once-decode|deterministic previous/next` -- tooling: ARS claim-registry internals
- regex: `Activity data|activity metadata|adjudication_activity|side channel|ambient filesystem|DA-DECISION|DA-REBUTTAL|HEALTH-CHECK` -- tooling: ARS cross-run activity logging
- regex: `^Gate \((emit|resume)\)|^Required/Recommended|^Required \(|^Receipt required|^Required, including|^Required Subsections|^Required Materials|^Required Content` -- non-rule: table cells and headings
- regex: `^See `references/` -- non-rule: pointer to another file
- regex: `methodology_reviewer_agent|devils_advocate_reviewer_agent|Who catches it` -- tooling: names ARS reviewer agents; the check itself is C-18 and O-57
- regex: `Version labels|Integration Lead|Research Lead|git author` -- off-topic: team protocol fragments quoted in other files
- regex: `Stage 3' runs under|three-gate evidence` -- tooling: ARS re-review gate implementation; O-51 keeps the principle
- regex: `Other modes under flag ON|flag is ON|fresh Claude Code session` -- tooling: ARS session-reset flag
- regex: `If required materials are found missing during transition` -- non-rule: lead-in to an ARS table
- regex: `Replay receives|Reopening marks only|The summary is advisory state memory` -- tooling: ARS replay semantics
- regex: `Always do at least deep-research quick|Must show Stage 4.5 passed|common workflow mistakes` -- tooling: ARS mode-advisor fragments repeated in SKILL.md
- regex: `The ordinary state machine is authoritative|never a legal transition` -- tooling: ARS state-machine precedence
- regex: `Its own-draft result|Both bind the identical|stales both|independent carriers|must re-enter the existing integrity and screening|render only in the single` -- tooling: ARS advisory reruns (O-14 keeps "re-run integrity after any change")

## Seat 1 sources

- file: `skills/nature-response/references/chinese-author-alignment.md` -- off-topic: Chinese-language author workflow (the user writes Vietnamese; S1-96 covers non-native English)
- regex: `^"The authors should|^"Figure X should|^"Page 5, line 3|^"Why don't the authors` -- non-rule: example reviewer comments quoted in a classification table
- regex: `While experiments on dataset X would be valuable|We don't have access to that dataset` -- non-rule: example sentence in a tone guide
- regex: `Do not quote the memory mechanically|writing memory` -- tooling: optional ML-paper writing-memory file not bundled
- regex: `job market|JMP|candidate's|sole-authored|Each essay|essays? must|share a common theme|hiring committees|job talk|dissertation|identify an important question, execute credibly` -- off-topic: job-market-paper and dissertation advice in econ-write
- regex: `grant application` -- off-topic: grant writing
- regex: `two-period model|infinite horizon|theory papers|For mixed theory-empirical papers|Every assumption should earn its place|use no more math than the insight requires` -- off-topic: theory-model advice; empirical finance revisions rarely build models
- regex: `Kai Wu|signature block|Signature is fixed|-review\.doc|Output must be \.doc|Letter to the Editor \(with the recommendation line|Do not modify, translate, or omit any line` -- house style: referee-report author's fixed signature and file format
- regex: `Normal mode \(all comments\)|High-level mode|high-level mode|Citation rules are mode-specific|Do not cite papers|Do NOT cite papers|Use \(a\), \(b\), \(c\) subpoints|The very first line of the report MUST be` -- house style: referee-report citation modes when writing a report as a reviewer
- regex: `boldsymbol|mathbf|zero vector|vector of zeros|IEEE templates|begin\{algorithm\}|variables that fall from the sky|seeds or runs|the agent achieves` -- off-topic: LaTeX math typesetting and ML-experiment checks from the proofreading skill (S1-68 keeps notation consistency)
- regex: `Exclude pure syntax tokens|Each category must open with a clear topic sentence|The problem statement must describe|New contributions should be supported by theorems|precisely list the new theoretical contributions` -- off-topic: CS/ML paper structure checks in proofreading (theorems, problem statements)
- regex: `Bets don't|Bets don.t have lifespans|Cultures don't shift|Conversations don't move|Markets don't reward|Complaints don't "become"|You don't sit down one day|What if I told you|The essay should move` -- non-rule: essay-style examples in stop-slop; the rule (false agency, meta-commentary) is S1-84 and S1-81
- regex: `Modified titles must NOT use colons|CRITICAL INTERACTION RULE|Do NOT flag for footnote conversion` -- house style: paper-polish interaction details
- regex: `description: This skill should be used` -- non-rule: skill front matter
- regex: `Do not generate a cover letter in the MVP|If the user asks for one, state that it is adjacent` -- house style: nature-response scope note (S1-43 lists the cover letter as a deliverable)
- regex: `Schema 11|Material Passport|Devil's Advocate|reviewer seats commit|synthesizer cannot|Stage 2\.5|Stage 4\.5|orchestrator only dispatches|after each pipeline stage prompt` -- duplicate: pipeline rules carried by core C-18/C-35 and the orchestrator card (O-23, O-24, O-35, O-51, O-53)
- regex: `Phase 1 - Parse \(atomize` -- non-rule: heading
- regex: `Do not present these as acceptable final responses:|Calibration anchors \(do not inflate\):|The abstract must follow this fixed four-part structure, in order:|The introduction must contain, in roughly this order:|Required fields present|^Every response row must include one of:$|Mix two concise forms` -- non-rule: lead-in to a list whose items are covered (S1-48, S1-103, S1-56, S1-57, S2-77, S1-35, S1-61)
- regex: `Most papers submitted to AER are rejected|Prior: "why should I care` -- non-rule: background statistic and persona prompt in aer-referee-sim
- regex: `Final papers should be no more than 35-45 pages|Target length: Standard empirical papers` -- house style: page-length targets vary by journal; the journal's limit applies (C-50)
- regex: `Do NOT emphasize methodology in title|Title: should be memorable|Avoid generic titles|Bad: "Essays on` -- off-topic: choosing a title for a new paper; titles rarely change in a revision
- regex: `It should occupy 20-30% of the introduction` -- house style: econ-write length heuristic for the literature paragraph
- regex: `The previous section covered how to format tables` -- non-rule: transition sentence
- regex: `Every empirical paper submitted to AEA journals|Code must reproduce all results without manual intervention|Never commingle code and data files` -- duplicate: replication package rules are S2-14

## Seat 2 sources

- regex: `tight_layout|constrained layout|Seaborn|Plotly|WebGL|MathJax|topojson|Kaleido|Matplotlib file timestamps|native_scale|categorical plot uses native|synthetic fixtures|Share Chart` -- tooling: Python plotting API details; open scientific-visualization when plotting in Python (TF-49 keeps "export at final size")
- regex: `blot|gel images|scale bars|microscopy|raw intensity data|clone, or enhance|preserve originals, disclose whole-image` -- off-topic: biological image integrity; finance figures are charts (TF-26 keeps "never alter data")
- regex: `number of cells|cells, fields|fields of view|spectra|technical replicates|cell-level violins|experimental hierarchy|clinical-trial|medical, regulatory` -- off-topic: lab-science replicate structure; the finance analogue is S2-72
- regex: `require_matplotlib_panel_alignment|panel_alignment\.R|audit_panel_alignment|gtable|width_ratios|row_groups|column_groups|--strict|NOT AUDITABLE|exit code `?2|spanning panel|equal-grid-span|unequal-span grids|global tolerance|delivery bundle|Supply valid measured geometry|REVIEW REQUIRED|marked PDF is a QA-only|Do not reuse a report from an earlier render|selected backend's figure|free-positioned hero panel` -- tooling: nature-figure's alignment-audit scripts, which this skill does not run (TF-42 keeps "aligned panels, inspect the rendered file")
- regex: `Extended Data|ED figure|corresponding author's surname|NMI|Nature Portfolio title|Nature Portfolio subjournals|Nature Communications|Scientific Reports|npj|Nature Reviews|Science Advances|AAAS|flagship|initial-review files separate|accepted-in-principle|^initial_submission$|production artwork` -- off-topic: Nature/Science submission logistics; TF-52 keeps "verify the target journal's live page"
- regex: `passport|/commit|quality_reports|locator|MEMORY\.md|Append only|Write with `>>`|exit 0|exit 1|sweep happens|review-paper --adversarial|summary-parity|/verify-claims|/audit-reproducibility|Stamp the revision|-dirty|pinned commits|committed `MEMORY|reconstructible from the repo|belongs to the project, rather than to your machine|influenced the result, it should be visible|Use fuzzy heuristics|teaching from the same numbers|Phase 5|Phase 4c|Hard floor|Never downgradable|EXPLAINED rows do NOT|UNMATCHED > 0|EXPLAINED claims do not halt|Should not appear in a submission-ready|UNVERIFIED\*\* — the claim was added` -- tooling: audit-reproducibility's passport and git-hook workflow; the rules are S2-10 to S2-15
- regex: `Land Registry|Zoopla` -- off-topic: data sources of one housing project
- regex: `StatsPAI|tool-bindings|MCP server` -- tooling: optional MCP estimator bindings
- regex: `Excel first|\.xlsx` report|in-memory verification data|re-parse the xlsx|Step 6|APPLY_FIXES|Do not undo prior edits` -- tooling: reference-verify's report and fix-queue implementation (S2-81 keeps the safety rules)
- regex: `It needs only the Python standard library and never compiles` -- non-rule: description of a bundled script
- regex: `export_plan\.py|scripts/export_plan` -- tooling: bundled planner script
- regex: `arxiv\.org/abs|version suffix such as `v1`|Always cite the current version` -- non-rule: citation instructions for the skill itself
- regex: `Kaleido 1\.4\.0` -- tooling: dependency note
- regex: `^Required action$|^Required diagnostics\.?$|^Required Diagnostics$|^Required contract$|^Required$|^Legend information each quantitative panel should provide$|^Ask whether source data should include:$|^Avoid accusatory phrasing:$|^should be clarified before submission$|^P0 — must fix before submission or resubmission$|^Every empirical AER paper should report, at minimum:$|^Do not present these as cross-publisher laws:$|^Avoid visual deception$|^For thin lines or required graphical objects on white|^Do not let the reader infer\.$|^Required families|What Notes Must Include` -- non-rule: headings or lead-ins whose list items are covered
- regex: `For each family: when it is required versus optional|"Required" means a referee will demand it|references/robustness-menu\.md` -- non-rule: description of the robustness menu file
- regex: `It is a local summary of sources|The skill should not pretend|It should instead enforce transparent reporting|This file should refine prose` -- non-rule: self-description of a source skill
- regex: `Read it together with the \[Nature Results|When figure order must follow the manuscript argument, also load|nature-shared` -- tooling: pointer to an unbundled file
- regex: `If the request is planning or auditing only, do not ask for Python or R|Reuse a choice already established|Do not guess or choose a backend by aesthetics` -- tooling: nature-figure backend-selection dialogue
- regex: `Do not mention private paths, source filenames` -- off-topic: privacy of draft provenance in figure text
- regex: `open for decision tree and per-design required diagnostics` -- non-rule: skill-index line in r-data.md
- regex: `Lines should be no thinner than 1 pt on that general page|Lettering should be about 7 pt after reduction|Lettering should be no smaller than 5 pt|Science explicitly advises` -- duplicate: journal-specific sizes are summarised in TF-37 and TF-49; the target journal's page wins
