# Tier 1 card: Deep search (tìm kiếm sâu, chính xác, cụ thể)

Load in full before any search for facts, laws, data or literature, and give it to every agent that searches. Rule IDs are `DS-xx`. The point is precision: an exact article and clause, an exact table and page, an exact dataset and variable. A strategy-level summary ("Việt Nam đang đẩy mạnh…", "nhiều nghiên cứu cho thấy…") is not a search result and never enters the proposal. Full multi-agent research pipeline: `skills/deep-research/SKILL.md`; fact-check mode: `skills/deep-research/SKILL.md` (mode fact-check).

## A. What counts as an answer

- **DS-01** Every searched fact is returned as a record: claim | exact value (number, date, name) | primary source (title, issuer/author, number or DOI, date) | locator (article, clause, point; table, page, paragraph) | verbatim quote ≤ 2 sentences | URL and access date | status KHỚP / LỆCH / CHƯA CÓ NGUỒN. A fact without locator and quote is UNVERIFIED (core C-12, C-33).
- **DS-02** Specific beats general: answer with the regulation number, the effective date, the variable name, the coefficient and its table, the sample years. If the only thing found is a general statement, report "chưa tìm được nguồn cụ thể" and add the item to the document request list (P-06); do not paraphrase the general statement into the proposal.
- **DS-03** Source hierarchy, highest first: (1) official primary text (Công báo, văn bản gốc có số hiệu, văn bản hợp nhất, quyết định của Sở giao dịch, statute, regulator rulebook); (2) official statistics or provider documentation; (3) the published peer-reviewed article (journal version with DOI); (4) working paper or thesis by the original authors; (5) reputable secondary (central bank reports, IMF/World Bank); (6) press, only as a lead to (1)–(5). Cite the highest level actually read.
- **DS-04** Two independent sources for any fact that drives a variable, a date in the design, a sample definition or a headline claim; when they disagree, report both with locators and ask the user (core C-36).

## B. Legal and institutional facts (Vietnam and abroad)

- **DS-10** Trace the full chain: original text → every amending text → the latest consolidated text (VBHN) → implementing decisions of the exchange or regulator → official announcements of schedules. Record for each: number, type, issuer, signing date, effective date, the exact article/clause/point used, and whether a later text amended it.
- **DS-11** Check effective dates against the study window year by year (core C-66); note transition provisions ("chậm nhất đến hết ngày…", "kể từ ngày…") verbatim.
- **DS-12** Vietnamese sources to try in order: vbpl.vn, congbao.chinhphu.vn, chinhphu.vn, the issuing ministry's portal (mof.gov.vn), ssc.gov.vn, the exchanges (vnx.vn, hsx.vn, hnx.vn), thuvienphapluat.vn (as a copy, then confirm the official text). Search with the exact number pattern ("139/2025/TT-BTC"), the subject in Vietnamese, and the clause wording.
- **DS-13** When a site is blocked or the text is a scan, do not substitute press; add the document to the request list with what part is needed.

## C. Literature

- **DS-20** Find the published version: DOI via Crossref or the publisher; record journal, year, volume, issue, pages. Working paper only if no published version exists, labelled as such. → core C-04, C-05
- **DS-21** Read the paper itself for anything cited as a finding: the sample, period, design, the exact estimate with its table, the direction and the caveat. A finding is cited with its locator ("Table 4, col. 2") in the search record. Abstract-only reading is recorded as such and is not enough for a numeric claim.
- **DS-22** Search systematically, not by one query: define the question, list keywords and synonyms in English and Vietnamese, search at least Google Scholar, SSRN/RePEc, the publisher or JSTOR, and Vietnamese journals; follow references backward and citations forward from the 3–5 closest papers; record queries, databases, dates and hits (this becomes the search-scope statement in P-12).
- **DS-23** Classics and frontier: for each design or concept used, identify the canonical source (the paper that defined the measure or estimator) and the current best-practice review; cite both when the proposal relies on them.
- **DS-24** Do not attribute to a paper what a summary says it found; mismatches between the summary and the paper are reported (example: a finding about investor sentiment misreported as a liquidity finding).

## D. Data

- **DS-30** For each dataset: provider, exact series or variable name, unit, frequency, coverage years and countries, access route (licence, cost, institutional subscription), update schedule, known breaks or methodology changes, and the documentation page. Mark "đã có / đang xin / chưa có".
- **DS-31** Verify that the data can actually produce the variable as defined (fields exist, frequency suffices, history long enough for the pre-period and post-period in the design).

## E. Search execution and reporting

- **DS-40** Use the deepest search mode available for niche, recent or legal facts (extended web search, full-text fetch of the primary page); run independent queries in parallel; never stop at the first page of results when the answer is not explicit.
- **DS-41** Never paste proposal text into external services; search with general keywords (core C-11 spirit; user privacy rule).
- **DS-42** Keep a search log (query | database | date | hits | kept | reason) in the working folder; it backs the search-scope claim and lets the next session continue instead of repeating.
- **DS-43** End each search task with three lists: verified records (DS-01), conflicts needing a user decision, and the document request list for the user (P-06 format: exact title, issuer/author, year, number/DOI, why, where used, which part, where to look, keywords VN/EN, priority). Repeat the open request list at the start of every round.

<!-- CARD-END deep-search v1 -->
