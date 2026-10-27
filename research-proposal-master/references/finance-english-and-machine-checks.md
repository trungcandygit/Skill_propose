# Finance English and machine checks (gaps 4 and 5)

Found by web search on 2026-10-23; the facts below come from registry listings and search snippets, not from reading the repositories line by line, except for the files that are bundled here and can be read directly.

## 4. Finance and economics English

What exists:
- `skills/econ-write/` (bundled; source: hanlulong/econ-writing-skill). Synthesises guidance by Cochrane, McCloskey, Shapiro, Head, Bellemare, Goldin and others; has `review-checklist.md`, `identification-strategies.md`, `latex-tips.md`, `specialized-tasks.md`. Best single starting point for empirical finance prose. The listing warns not to copy its template sentences word for word.
- McCloskey, *Economical Writing* (3rd ed., University of Chicago Press, 2019): 35 rules from the big picture down to the word. A book, so it is not bundled; buy or borrow it.
- Manchester Academic Phrasebank (University of Manchester website): general academic phrases by section (introduction, methods, results, discussion). It is not finance-specific. The search returned many scraped mirrors on unrelated domains, so use only the official university site.
- Not found: a finance-specific phrasebank (asset pricing, banking, valuation). The closest bundled material is `skills/master-academic-paper-skill/reference_phrasebanks/` and `skills/nature-writing/`.

How to use them in a revision:
1. Draft or fix the paragraph with `skills/econ-write/` conventions (claim first, one idea per paragraph, concrete numbers, no hedging on own results).
2. Replace generic openers using the phrasebank files; keep terminology fixed (do not rotate synonyms for the same variable).
3. Run the anti-slop pass (`skills/stop-slop/`, `skills/humanizer_academic/`) on the new text only.
4. For Vietnamese-first authors, add a grammar pass with `skills/claude-writer-minhuw/skills/grammar-checker/` and `skills/claude-writer-minhuw/skills/polish/` (articles, prepositions, tense, sentences translated word for word from Vietnamese).

## 5. Machine verification of results

These replace "I re-read it" with something executable. Run on copies of the data and outputs.

| Check | Open | What it does (from its own SKILL.md) |
|---|---|---|
| Numbers in the manuscript vs actual R/Stata/Python outputs | `skills/audit-reproducibility/` (+ `rules/replication-protocol.md`, the tolerance thresholds) | Extracts point estimates, SEs, p-values and counts from the manuscript, compares to the output files, reports PASS/FAIL per claim against tolerances. |
| Every table and figure traced to a script and output | `skills/audit-replication/` | Script syntax, output freshness, file integrity, dependency and provenance checks, README completeness in AEA format. Written for one specific project, so adapt paths before use. |
| Reproduce results end to end | `skills/replicate-compound/`, `skills/stata-replication/` | Structural checks (seeds, versions, paths) and functional checks (reproduction, environment, output match). Stata needs a licence and a stata-mcp server. |
| Package for the AEA / openICPSR deposit | `skills/replication-package-aea/`, `skills/aer-replication/` | README, dataset manifest, computational requirements, table-to-script map. |
| R code review | `skills/review-r/`, `skills/data-analysis-r/` | Code quality and the standard analysis pipeline. |
| Bibliography entries | `skills/validate-bib/`, `skills/reference-verify/` | Existence and metadata of each BibTeX entry. |
| Challenge the main claim | `skills/devils-advocate/` | Adversarial questions on design and claims. |

Not covered by anything found:
- statcheck-style recomputation of p-values from reported test statistics. It exists as an R package, but this search did not confirm it as a skill; if needed, install it in R and run it on the reported statistics.
- reproducr (CRAN) audits R scripts for reproducibility risks such as stochastic calls without `set.seed()`. It does not compare manuscript numbers with tables.
- Plagiarism and similarity checking; use the university's licensed tool.

Rule for the verification panel (`references/panel-protocol.md`): anything in this table that can be run must be run by script, not judged by reading. If a script cannot run (missing data, licence), the item is UNVERIFIED, never PASS.
