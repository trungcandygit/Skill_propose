# Response letter: fill-in template and routing

Use this after the manuscript has been revised (see `revision.md` Phase 4). Rules for tone and honesty are in `revision.md` (Hard rules: Completeness, Tone). This file adds a ready English template and says where the longer pattern libraries are.

Bundled sources, open only if you need more examples:
- `skills/review-response/references/rebuttal-templates.md`, `response-strategies.md`, `tone-guidelines.md`, `successful-cases.md`
- `skills/nature-response/references/response-structure.md`, `action-mapping.md`, `difficult-cases.md`, `qa-checklist.md`
- `skills/aer-rebuttal/references/response-letter-patterns.md` (economics R&R)
- `skills/referee-response/SKILL.md`, `skills/rebuttal-writing/`, `skills/paper-referee-revise/SKILL.md` (long verbatim response with red-marked excerpts)
- `skills/academic-paper/` revision-coach and rebuttal-audit modes (check an existing draft letter against the comments)

## 0. Pick the format

| Situation | Format |
|---|---|
| Economics or finance journal, R&R | English letter, Part 3 below; follow the journal's own instructions first |
| Conference or short rebuttal with character limits | `skills/rebuttal-writing/` |
| Reviewer asked for new regressions | Letter plus attached tables; read real numbers from the table files, never from memory |

## 1. Before writing

1. The manuscript is already revised and the numbers in it are final (the letter quotes page, line, table numbers that must exist).
2. The tracker has one row per comment with its status (answered, partly, declined with reason, needs author input).
3. Decisions are made: accept, clarify, defend, or run new analysis (`revision.md` Phase 3). Never write a reply for a comment whose decision is still open.

## 2. Tracker (keep this table, it feeds the letter)

| ID | Reviewer text (verbatim) | Type | Decision | Change in manuscript | Where (section, page, line, table) | Evidence | Status |
|---|---|---|---|---|---|---|---|
| R1.1 | ... | Major | Accept | New robustness check | Sec. 5.3, Table A4 | Table A4 col 3 | done |

Status values: `done`, `partly`, `declined (reason)`, `AUTHOR_INPUT_NEEDED`. Anything not `done` must be visible in the letter.

## 3. English letter template

```
[Date]

Dear Professor [Editor],

Thank you for the opportunity to revise our manuscript "[Title]" (Manuscript ID [..]).
We are grateful to the editor and the [N] referees for their constructive comments.
The main changes are: (1) [one line], (2) [one line], (3) [one line].
Convention: referee comments are in italics, our responses in plain text; page and line
numbers refer to the revised manuscript. Changes are highlighted in [colour] in the
marked-up file; a clean file is also attached.

RESPONSE TO THE EDITOR
E1. [quote]
Response: [action first]. [evidence]. [location].

RESPONSE TO REFEREE 1
R1.1 [full quote, not trimmed]
Response: [We agree / We respectfully disagree / We clarified]. [What we changed and where,
in the first two sentences.] [Evidence: table, figure, number from the table file.]
[Location: Section x, p. y, lines a-b, Table z.]

R1.2 ...

RESPONSE TO REFEREE 2
...

SUMMARY OF MAJOR CHANGES
1. ...
2. ...

NEW MATERIAL ADDED
Table A4 ..., Figure 5 ...

Sincerely,
[Authors]
```

Wording that works:
- Agree: "We thank the referee for this suggestion. We now [do X] (Section 5.3, Table A4). The estimate is [value] ([SE]), consistent with the baseline."
- Clarify: "This result was in the original submission but easy to miss. We moved it to Section 4.1 and added a cross-reference (p. 12, lines 3-8)."
- Respectfully decline: "We appreciate the concern. [State the boundary exactly: why the request is outside scope or based on a different premise.] [Point to existing evidence.] To help readers, we added a sentence in the Discussion (p. 20, lines 5-9)."
- Soften a claim: "We agree our wording was too strong. The text now says 'is consistent with' (p. 3, line 14)."

Avoid: "The reviewer misunderstood", "Thank you for the comment" with nothing after, "We have revised accordingly", "we will consider", promises of future work for a blocking comment, hiding a concession in the passive voice.

## 4. After drafting

1. Run the anti-slop pass (`skills/stop-slop/`) on the letter, not on the quoted reviewer text.
2. Machine checks: every page, line and table reference resolves in the revised file; every number in the letter equals the table file; every comment ID in the tracker appears in the letter.
3. Send the letter and the revised manuscript through the two-agent panel in `panel-protocol.md` (Agent 1 checks coverage and honesty of "we revised", Agent 2 checks numbers and citations).
4. Deliver a marked-up manuscript, a clean manuscript, the letter (.docx or .tex), and any new tables. If the user wants Word output, use the installed office skills or Pandoc.
