# Sources added for the proposal edition (Gate 0 record, maintain M-10)

Base: `paper-revision-master` from trungcandygit/SKILL_ACADEMIC @ 8970560 (snapshot 2026-10-23), renamed `research-proposal-master` on 2026-10-27. Journal-format rules removed on user request: TF-48, TF-49, TF-51, TF-52, TF-54, TF-60, TF-61, O-65, O-66, S1-114 and `references/journals/`. IDs are not reused.

| Skill (under `skills/`) | Origin | Licence | Network / scripts | Used for |
|---|---|---|---|---|
| research-grants | K-Dense-AI/claude-scientific-skills (v1.3) | MIT | optional figure script calls OpenRouter: not used | proposal P-01, P-02, P-10, P-11, P-13, P-20, P-40 to P-45, P-70, P-74 |
| proposal-revise | chrisblattman/claudeblattman @ 12e14d4 | MIT | none (Google Workspace line ignored) | P-81 |
| review-pap | claesbackman/AI-research-feedback @ d129756 | no LICENSE file recorded; keep private use in mind | none | P-21, P-30, P-31, P-35, P-36, P-43, P-72 |
| credible-claims | pedrohcgs/claude-code-my-workflow @ ae72617 | MIT | none | P-72 |
| statistical-power | K-Dense-AI/claude-scientific-skills @ a1043ef5 | MIT | scripts/power.py not run (unread) | P-33 |
| mhe-identification | franklee16/academic-research-skills @ 9a4b2db2 | no LICENSE file (frontmatter says MIT) | none | P-30, P-32 |
| skill-creator | anthropics/skills (copy from /mnt/skills/examples) | Apache-2.0 (LICENSE.txt) | eval scripts not run | maintain card |
| research-proposal | luwill/research-skills @ 2b6f5bc (~876 stars) | MIT stated in README; no LICENSE file | scripts/check_proposal.py, integrity_gate.py: local only, no network (read imports); tests use subprocess, not run | P-90 to P-96, P-102 |
| grant-proposal (+ templates/) | pedrohcgs/claude-code-my-workflow @ ae72617 (~1.7k) | MIT (LICENSE.upstream) | none; refers to `.claude/rules/*` and a claim-verifier agent of its home repo, which are not bundled | P-92, P-97 to P-99 |
| preregister | pedrohcgs @ ae72617 | MIT | none | P-100 |
| power-analysis | pedrohcgs @ ae72617 | MIT | generates R/Stata/Python power scripts on request | P-101 |
| interview-me | pedrohcgs @ ae72617 | MIT | none | P-92, P-103 |
| data-management-plan | pedrohcgs @ ae72617 | MIT | none | P-98 |
| writing-skills | obra/superpowers @ 2ce8aa1 (~306k) | MIT (LICENSE.upstream) | render-graphs.js not run; expects superpowers:test-driven-development | maintain M-40 to M-43 |
| aer-preregistration, deep-research and the rest | already in the base bundle | see base README | — | P-21, P-33, P-34, P-37; deep-search card |

Rules also distilled from the user's own standing rules in the M-n_HTTM proposal project (2026-10): `[CẦN XÁC MINH]` marking, APA "&"/"và", no tracked changes, primary-text verification of legal chains (TT57 → TT69 → TT139), document request lists, repository privacy check.
