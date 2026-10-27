## Workflow: phân tích dữ liệu bằng R

Source tags: [DC]=data-cleaning [EA]=empirical-analysis-r [TV]=tidyverse-patterns [ES]=econ-stats [OLS]=ols-regression [PD]=panel-data [DID]=did-analysis [IV]=iv-estimation [RDD]=rdd-analysis [SC]=synthetic-control [TS]=time-series [CIM]=causal-inference-mixtape [ME]=marginaleffects [PF]=pyfixest [AID]=aer-identification [AROB]=aer-robustness [ATF]=aer-tables-figures [ET]=econ-table [EF]=econ-figure [GG]=ggplot2 [NF]=nature-figure [SV]=scientific-visualization [PH]=phack-detection [SS]=specification-search [RS]=r-style-guide [RP]=r-performance

0. (Optional, pre-data) Pre-Analysis Plan: power/MDE (pwr, WebPower, DeclareDesign), freeze outcomes + spec in pap/strategy file; register RCTs with AEA RCT Registry BEFORE intervention. [EA][AID]
1. Route card: record mode (econ/epi/ML-causal), estimand, design, focal outcome/treatment, packages, required artifacts; ask data source, unit of observation, key variables, known quality issues. [EA][DC]
2. Project skeleton: raw/ (never overwrite), artifacts/, tables/, figures/, renv lockfile, set.seed(), master.R with house-style wrapper; Quarto for narrative + code. [EA][DC]
3. Import: haven::read_dta / readr / data.table::fread / arrow; janitor::clean_names(); skimr::skim(), naniar::miss_var_summary()/vis_miss(). [EA]
4. Dtypes: set integer year, numeric, factor, Date explicitly. [EA]
5. Missing: decide PER VARIABLE; recode sentinel codes (-99, -88) to NA first; drop_na only on key vars; add *_missing flag when imputing; test MCAR (is y-missing related to covariates?) -> if not MCAR use mice/IPW not listwise. [EA][DC]
6. Outliers: flag first (|z|>4), do not drop silently; winsorize (1/99, document percentiles; optionally within industry-year) rather than delete. [EA][ES]
7. Duplicates: stopifnot(nrow(distinct(df, id, year)) == nrow(df)) BEFORE any merge. [EA][DC]
8. Merge: join_by() + relationship="many-to-one" (declare cardinality), unmatched="error", na_matches="never"; assert nrow unchanged; tidylog:: interactively. [TV][EA]
9. Sample-construction log (tibble step/n after each filter) -> write JSON, paste as data-section footnote. [EA]
10. Five-check data contract before modeling: shape, dtypes, missingness, duplicates on keys, panel balance (+cohort sizes, y range, treatment share); stopifnot() fails => stop and fix in dplyr. [EA]
11. Construct variables: log(pmax(x,1)) or asinh() for zeros (never log(0)); deflate nominal by CPI to base year; arrange(id, year) THEN group_by(id) for lag/lead/diff; first_treat, rel_time = year - first_treat, never_treated flag for staggered DiD. [EA][OLS]
12. Write the estimating equation + one-sentence identifying assumption + auto-flagged threats + fallback estimators BEFORE estimating (strategy.md, git SHA frozen). [EA][AID]
13. Pick design with decision tree: running var+cutoff -> RDD; instrument -> IV; pre/post x treat/control -> DiD (staggered -> CS/SA/BJS); 1 treated unit + donors + long pre -> SCM; high-dim X selection-on-observables -> DML/matching + sensitivity. [EA][AID]
14. Descriptives (Table 1): N, mean, SD (min/max/median); panel dims N units, T periods, N*T; balance with normalized differences; % missing per variable; correlation matrix; distribution + trend plots. [ES][EA]
15. Identification graphics BEFORE regression table: event study / first stage / RD binned scatter + density / SCM trajectory; pair figure with numerical test (joint Wald on pre-period leads). [EA][DID]
16. Baseline diagnostics on pooled OLS: bptest (het), dwtest/bgtest/Ljung-Box (autocorr), vif (collinear), RESET (spec), pbgtest + pcdtest (panel), phtest (FE vs RE), adf/kpss (time series). Choose SE from the test results. [EA][OLS][PD]
17. Baseline model: fixest::feols with absorbed FE + cluster at level of treatment variation; progressive columns M1->M6 (raw, +demographics, +controls, +unit FE, +two-way FE, +interacted FE e.g. industry^year). [EA][ATF]
18. Design-specific estimator (modern, not TWFE for staggered): att_gt / sunab / did_imputation; ivreg/feols IV with AR; rdrobust; synth/augsynth/synthdid. [AID][EA]
19. Robustness battery: alt specs, samples, outcome definitions, clustering, estimators, outliers; placebos; sensitivity (HonestDiD, Oster delta, E-value); spec curve if contested. [AROB][EA]
20. Further analysis: heterogeneity (theory-predicted interactions, marginaleffects::avg_slopes), mechanism/outcome ladder, triple-diff, CATE (grf) only if pre-specified. [EA][AROB][ME]
21. Tables: Table 1 balance, Table 2 main M1-M6, Table 3 mechanism, Table 4 heterogeneity, Table 5 robustness; export .tex + .docx + .xlsx from one call. [EA][ATF]
22. Figures: F1 trend, F2 event study (ref -1, 95% CI), F3 coefplot across specs, F4 sensitivity/spec-curve; export PDF (vector) + PNG >=300 dpi. [EA][EF]
23. Hygiene gate: p-hacking / spec-search audit of the reported specification vs the full universe; log accepted/rejected patterns in analysis_log.md; replication bundle (code, sample_log, contract JSON, sessionInfo). [SS][PH][EA]
24. Execution gate (SkillOpt style): change ONE decision at a time (sample rule / estimator / clustering / export / check); define held-out gate first (row counts, key uniqueness, treatment support, missingness thresholds, expected output files, one non-focal robustness spec); on failure revert to last passing spec and log; promote to boilerplate only after passing on alternate outcome/sample. [EA]

## Hard rules

### Data
- NEVER overwrite raw data files. [DC]
- ALWAYS check duplicates before merging; assert row count after merge (no row inflation). [DC][EA]
- ALWAYS handle missing-value codes (-99, -88, ...) before computing anything. [DC]
- ALWAYS label variables/values and keep a data dictionary/codebook; document every transformation (explain WHY). [DC]
- Use assert/stopifnot early; R estimators silently drop NA rows downstream (N falls without warning) -> contract check upstream. [DC][EA]
- Never log-transform zeros: use asinh() or log(x+1) with interpretation stated; ln(0) undefined. [OLS][EA]
- Panel lags/leads: arrange(id, time) and group_by(id) first, else lag is non-deterministic. [EA]
- Outliers: flag, then winsorize/trim with disclosed percentiles; never drop silently. [EA][ES]
- Report sample restrictions and winsorization in notes ("winsorized at 1st and 99th pct"). [ES]
- Mean of skewed variables (income, firm size) misleads: report median or log. [ES]
- Always report % missing per variable. [ES]
- Never use NA-unsafe negated filters: negation silently drops NA -> use filter_out()/explicit NA handling (dplyr 1.2). [TV]
- Prefer join_by() over by=c("a"="b"); never use sapply (use map_*); no `:=` string-built names in data masking. [TV]

### Estimation / inference
- OLS with controls does NOT establish causality; causal claim needs IV/DiD/RDD/SCM identification. [OLS]
- Never control for post-treatment variables / mediators (bad controls, collider bias). [OLS]
- Default OLS SE is valid only under homoskedasticity; use HC (cross-section), cluster (grouped), Newey-West/HAC (time series). [OLS]
- Always state SE type in the table note; cluster at the level of treatment variation, not the individual by reflex. [PD][DID][ET]
- R-squared is not evidence of correct specification or causality. [OLS]
- Hausman p<0.05 => FE; never use RE without testing; FE coefficients are within-unit only and cannot estimate time-invariant regressors. [PD]
- Always say which FE (entity, time, both) are included; report F-test for joint FE significance and Hausman result. [PD]
- Lagged DV with FE in short T => Nickell bias; use Arellano-Bond/system GMM, report AR(1) sig, AR(2) insig, Hansen p>0.05, restrict lag range (instruments <= N; proliferation weakens Hansen). [PD]
- Macro panels (small N, large T): FE SE invalid under cross-sectional dependence -> Driscoll-Kraay. [PD]
- Few clusters (<50, esp. <30) => wild cluster bootstrap p-values (fwildclusterboot::boottest); <15 clusters is a pathology flag. [ATF][AROB][SS]
- Never regress non-stationary series on each other (spurious); test unit roots first; never VAR in levels with I(1) and no cointegration. [TS]
- Granger causality = predictive content only, not causation. [TS]
- Ignoring structural breaks mimics a unit root: use Zivot-Andrews. [TS]
- Multiple primary outcomes => FWER correction (Romano-Wolf). [AID][AROB]
- ALWAYS present Table 2 as multi-column progressive spec (M1->M6); same coefficient row across columns. [EA][ATF]

### Causal designs
- TWFE with staggered adoption and heterogeneous effects is BIASED (can flip sign): use Callaway-Sant'Anna, Sun-Abraham, BJS imputation, dCDH; show Goodman-Bacon decomposition. [AID][DID][CIM]
- TWFE acceptable only if simultaneous timing + never-treated control + implausible heterogeneity. [AID]
- "Control group" of eventually-treated units is a red flag. [AID]
- Failing to reject pre-trends != parallel trends (low power): joint test + Roth (2022) power + HonestDiD bounds. [DID][AID]
- Pre-trends must be a JOINT test, not just a plot. [AID]
- Always show event-study figure for DiD (ref period -1, pre-periods visible). [DID][EF]
- Consider anticipation/Ashenfelter dip/spillovers. [DID]
- First-stage F>10 rule is OBSOLETE; F=12 is not evidence of strength; F<50 => AR confidence sets required; use effective F (Olea-Pflueger)/ivDiag. [AID]
- Exclusion restriction cannot be tested: state in one sentence in intro, defend with narrative + placebo + sensitivity (Conley); "we control for X" is not a defense. [AID][IV]
- IV estimates LATE for compliers, not ATE; show OLS alongside IV; report first stage; Sargan only if overidentified. [IV]
- Bartik/shift-share: pick shares-exogeneity (Rotemberg weights, top-5 industries) OR shocks-exogeneity (shock-level inference); do not hand-wave between them. [AID]
- RDD: local linear, triangular kernel, MSE-optimal (CCT) bandwidth, robust bias-corrected CI; NO global high-order polynomials (order>1 discouraged; order 4 is a red flag). [AID][RDD]
- RDD: always show binned scatter; failed density test = design compromised; never extrapolate away from cutoff; bias-corrected estimate with conventional SE is a flagged combination. [RDD][SS]
- SCM: pre-treatment fit is foundation (pre-RMSPE < ~5% of pre-mean); inference by placebo (in-space, in-time), never default SEs; report full donor pool + weights; donors >10% weight discussed. [SC][AID]
- SCM with many treated units: not Synth; use augsynth/gsynth/synthdid. [CIM][SC]
- PSM requires common support check and covariate balance table. [IV][CIM]
- Using more than one identification strategy as independent confirmation when they share identifying variation is an anti-pattern. [AID]
- Identifying assumption goes in the introduction, not a footnote. [AID]
- Do not report OLS-with-controls as main and IV/RD as "robustness". [AID]

### Robustness / hygiene
- Heterogeneity must be theory-predicted (interaction form), labeled pre-specified vs exploratory; no heterogeneity by every demographic. [AROB]
- Null results: demonstrate power and tight CI; never claim "no effect" when it is "no precisely estimated effect". [AROB]
- Always report 95% CIs with p-values; prefer effect sizes over stars. [AROB]
- Never add robustness the morning before submission; never highlight 2 of 20 specs; never "available upon request". [AROB]
- Mechanism evidence must not contradict main sign on a subsample while presented as confirming. [AROB]
- Balance tests: use normalized differences (|Delta| < 0.25), not t-tests (large N makes everything significant). [ES]
- Specification search: the ledger must be complete; refuse to output "the winning spec" without it. [SS]
- Direction matters: if hypothesis has a sign, audit one-sided; two-sided audit understates multiplicity 2x. [SS]
- Null scheme must preserve structure: panel unit-level/staggered => cluster_permute (whole treatment path), never plain permute (null too tight). [SS]
- A "best specification" carrying pathology flags is not a finding; report best-unflagged. [SS]
- p-hacking tests operate on distributions of many results; NEVER assert an individual paper is p-hacked; a flag is a reason to look. [PH]
- Clean p-curve report from small collection (<~50) means little; shape tests need >=15 significant results. [PH]
- Naive caliper test gives false positives when true effects exist; use counterfactual version. [PH]
- Selection between stages (continuation) is not manipulation; use phase_shift_test/continuation_decomposition. [PH]
- Do not hand-roll when validated tool exists (callaway_santanna, ivreg+AR, rdrobust, synth+placebo, wild bootstrap, honest_did, oster_delta, evalue). [AID][AROB]
- Pre-registered spec null while best spec significant = fragility result; report it. [SS]

### Output
- Every table: SE structure, sample, N, significance legend in note; no stars without definition. [ET][ATF]
- No pie charts, no 3D, no default themes, no raster for line plots, never point estimates without uncertainty. [EF][ATF]
- Never alter/hide/invent/selectively enhance data to improve a figure; no silent line connection across missing values. [SV]
- If the design does not support a figure (cross-section -> no event study), message() why; do not silently drop. [EA]
- Every table in .tex + .docx + .xlsx; every figure PDF + PNG >=300 dpi (default output contract). [EA]

## Method cards

### OLS / linear models [OLS][ES]
- Assumptions: linearity, random sampling, no perfect collinearity, E(e|X)=0 (violation = bias -> IV/design), homoskedasticity (violation affects SE only), normality only for small-N inference.
- R: fixest::feols(y ~ x + controls, cluster=~g); lm_robust (estimatr); sandwich::vcovHC "HC3"; lmtest::coeftest.
- Diagnostics: Breusch-Pagan/White (het) -> robust SE; DW/Breusch-Godfrey -> Newey-West; VIF>10 -> drop/combine; Jarque-Bera/Shapiro (bootstrap if small N); RESET (misspec).
- Report: coef + SE in parentheses, SE type, N, R2/adj R2, F; equation written explicitly; log vs level choice; Oster delta for controls stability; interpret magnitude economically.
- Pitfalls: bad controls, causal language without design, default SE with clustered data, ln(0).

### Panel FE / RE / dynamic [PD][EA]
- Assumptions: FE = strict exogeneity conditional on alpha_i (within variation); RE = alpha_i uncorrelated with X; Mundlak/CRE adds unit means of time-varying X to RE.
- R: fixest::feols(y ~ x | id + year, cluster=~id); plm (model="within"/"random", phtest, pbgtest, pcdtest); high-dim interaction FE `industry^year`.
- Diagnostics: Hausman (p<0.05 -> FE); Wooldridge serial-correlation (pbgtest); Pesaran CD (pcdtest); F-test of FE; Arellano-Bond AR(1)/AR(2) + Hansen/Sargan (GMM; plm::pgmm or system-GMM), instrument count <= N.
- SE table: serial corr -> cluster entity; cross-sectional dependence -> Driscoll-Kraay; both -> two-way cluster; het only -> HC.
- Report: N units, T, total obs, balanced/unbalanced; FE indicators (Yes/No rows); cluster level; Hausman; GMM: instrument count, AR(1)/AR(2), Hansen p.
- Pitfalls: Nickell bias (FE + lagged DV, short T), wrong cluster level, FE as between effect, time-invariant var absorbed.

### DiD incl. staggered [DID][AID][EA][CIM]
- Assumptions: parallel trends (conditional on X), no anticipation, SUTVA/no spillovers; staggered: group-time PT, stable treatment (no reversal unless estimator allows).
- 2x2: feols(y ~ i(treated, post, ref=0) | id + year, cluster=~id). Event study: feols(y ~ i(rel_time, ref=-1) | id + year) ; iplot().
- Staggered (do NOT use plain TWFE): did::att_gt(control_group="nevertreated", est_method="dr") + aggte; fixest::sunab(first_treat, year); didimputation::did_imputation(horizon, pretrends); DIDmultiplegt; synthdid; bacondecomp::bacon for weights on forbidden comparisons.
- Diagnostics: Bacon decomposition; event-study with 95% CI; joint Wald pre-trend test (+ Roth 2022 power); HonestDiD::createSensitivityResults (Rambachan-Roth); cohort heterogeneity.
- Robustness: placebo dates (1-2+ periods earlier), placebo groups, alternative controls, continuous-dose DiD, wild bootstrap if few clusters.
- Report: figure (event study) is mandatory; coefficient with SE clustered at treatment-assignment level (state if policy at state); state estimand (ATT, dynamic horizon); explain why CS/SA/BJS chosen; discuss anticipation, Ashenfelter dip, spillovers.

### IV / 2SLS [IV][AID][EA]
- Assumptions: relevance, exclusion, independence/as-good-as-random, monotonicity (LATE). Estimand = LATE for compliers.
- R: fixest::feols(y ~ X | D ~ Z, cluster=...); summary(iv, stage=1); fitstat(iv, ~ ivf + ivwald + sargan); AER::ivreg(..., diagnostics=TRUE); ivDiag / weakivtest equivalents for AR + effective F; LIML as alternative.
- Diagnostics: first-stage F (effective F, Olea-Pflueger), AR confidence sets (primary under weak IV; mandatory F<50), Wu-Hausman (endogeneity), Sargan-Hansen (overID only), placebo regression where Z predicts outcome it should not, Conley plausibly-exogenous sensitivity, Rotemberg weights (Bartik).
- Report: first stage table with F; OLS vs IV side by side (direction of bias); exclusion restriction in one sentence + defense; LATE interpretation; SE clustering for shift-share per exposure structure; instrument sets compared (2SLS vs LIML).
- Pitfalls: F-only strength claim, untested exclusion, adding instruments without validity, ATE/LATE confusion.

### RDD [RDD][AID][EA]
- Assumptions: continuity of E[Y(0)|X], E[Y(1)|X] at cutoff; no manipulation of running variable; no other discontinuities. Sharp: ATE at cutoff; fuzzy: LATE = reduced form / first stage.
- R: rdrobust::rdrobust(y, x, c, kernel="triangular", bwselect="mserd", fuzzy=D); rdplot (state binning method); rddensity (Cattaneo-Jansson-Ma); rdbwselect.
- Diagnostics (all required): density/manipulation test; covariate balance at cutoff; placebo cutoffs; bandwidth sensitivity at 50/75/125/150% of optimal (>= 3 bandwidths); donut RDD if bunching; polynomial order robustness.
- Report order: binned scatter -> main estimate (CCT bw, triangular, local linear, robust bias-corrected CI) -> sensitivity table -> validity tests -> N total and N within bandwidth left/right. Covariate-adjusted result only as efficiency add-on; main must hold without.
- Template: "local linear regression with triangular kernel and CCT optimal bandwidth h=[X]; estimate [b] (SE, p)."
- Pitfalls: global polynomials, one bandwidth, extrapolating, ignoring failed density test.

### Synthetic control [SC][AID][EA]
- Assumptions: no interference (SUTVA), no anticipation, treated unit in convex hull of donors, stable DGP; need >=10 pre-periods, large plausible donor pool, aggregate intervention.
- R: Synth::synth, tidysynth, augsynth (progfunc="Ridge" if imperfect fit), gsynth (multiple treated), synthdid::synthdid_estimate (SDID, Arkhangelsky 2021), SCtools for placebos.
- Predictors: pre-treatment outcome lags (3-5 evenly spaced; too many overfit) + covariates; exclude donors with similar treatment/contamination; keep structurally similar units.
- Diagnostics: pre-RMSPE < ~5% of pre-mean; covariate balance table; in-space placebo (every donor as treated) + post/pre MSPE ratio rank p-value ("ranks 1st of 20"); in-time placebo (fake date); leave-one-out donors; Fisher/permutation inference.
- Report: treated vs synthetic path; gap plot with treatment line; donor weights table (donors >10% discussed); predictor balance table; placebo plot with treated highlighted; MSPE ratio p; full donor pool listed.
- Pitfalls: poor fit, cherry-picked donors, interpolation bias, using Synth for many treated units.

### Time series [TS][EA]
- Workflow: plot level/diff/log + ACF/PACF -> unit root (ADF H0 unit root; KPSS H0 stationary) -> model -> residual checks -> forecast.
- Test logic: ADF rejects & KPSS not => I(0); both non-stationary => difference & retest; conflict => check structural breaks (Zivot-Andrews).
- Decision: all I(0) -> VAR levels; all I(1) no coint -> VAR differences; I(1) + coint -> VECM (Johansen/Engle-Granger); mixed orders -> ARDL bounds test.
- R: tseries::adf.test/kpss.test, urca::ur.df, forecast::auto.arima/Arima, vars::VAR/VARselect, vars::causality, rugarch/fGarch for ARCH/GARCH (volatility clustering, finance data), lmtest::coeftest + sandwich::NeweyWest.
- ARIMA: AR(p) PACF cuts at p; MA(q) ACF cuts at q; AIC for forecasting, BIC for parsimony; Ljung-Box on residuals; CUSUM stability.
- Report: orders of integration, lag selection criterion, IRFs with bands, holdout RMSE/MAE + horizon + CI for forecasts.
- Pitfalls: spurious regression, levels VAR with I(1), too few/many lags, Granger != causal, ignored breaks.

### Marginal effects / interpretation [ME]
- Five questions: Quantity (predictions/comparisons/slopes) -> Grid (datagrid, observed vs counterfactual) -> Aggregation (by=, weights) -> Uncertainty (delta, robust/cluster vcov, bootstrap via inferences()) -> Test (hypothesis=, equivalence).
- R: avg_comparisons() for ATE/risk difference, avg_slopes() for AME (logit/feglm), predictions()/plot_predictions(), hypotheses(); G-computation for ATT/ATU via counterfactual grids.
- Coefficients of nonlinear models/interactions are not effects: transform into estimands before reporting.

### Python FE reference [PF] (only if switching to Python)
- pf.feols / fepois / feglm / quantreg; `y ~ x | fe1 + fe2`, IV `y ~ x | fe | d ~ z`; vcov default CRV1 on first FE; event_study, did2s, lpdid, etable, dtable; use `.vcov({"CRV1":"g"})`; wildboottest for few clusters.

## Tables & figures standards

### Table layout (modelsummary / etable / booktabs) [ATF][ET][EA]
- booktabs only (\toprule \midrule \bottomrule), no vertical lines; caption ABOVE tables, BELOW figures.
- Main table 3-7 columns (<= ~6), progressive simple -> rich; referee quotes column 4-5; same point-estimate row throughout; > ~7 main-text tables = unfocused -> appendix.
- Order rows: treatment first, then interactions/mechanism, controls last (or omit to appendix). Descriptive labels ("Household Income, 2017 USD"), never variable codes (coef_map / coef_rename).
- Indicator rows (Yes/No) for Controls / Unit FE / Year FE / Sample; N and R2 (or pseudo-R2, first-stage F) for every column.
- SE in parentheses below coefficients; never mix brackets and parentheses; clustering/HAC stated in NOTE not header.
- Stars: AER legend `* p<0.10, ** p<0.05, *** p<0.01` (c("*"=.1,"**"=.05,"***"=.01)); letter superscripts acceptable; do not mix across paper; AER discourages relying on stars - magnitudes matter; always define stars in note.
- Decimals: 3 for coefficients/SE, 0 for N; consistent across rows; precision matched to 2-3 significant digits of SE.
- Few clusters -> wild bootstrap p-values; weak IV -> AR CIs next to / instead of SE.
- Five canonical tables: summary stats (<=15 rows, N/mean/SD/min/max), variable definitions (appendix), balance/first-stage, main result, robustness/heterogeneity consolidated. Heterogeneity as interaction coefficients, not many subgroup tables (unless the point).
- Robustness table: first column = main-table estimate; one row/column per check; flag N changes; one main-text robustness table, rest in appendix (order: specs/clustering, samples/outcomes, heterogeneity, placebo/falsification, mechanism, theory, data appendix).
- Notes must state: estimator, SE structure/cluster level, sample, N (obs and clusters), star legend, FE/controls, data source, sample period, definitions. Keep notes concise; put equations in methods.
- LaTeX hygiene: generate BODY-ONLY file with full \begin{table}...\end{table} (no \documentclass) for \input{}; also standalone for spot-check; avoid siunitx S columns (use c / dcolumn D{.}{.}{-1}); no raw Unicode (>=, ->) in generated .tex (use $\geq$, $\rightarrow$); >=7 columns -> landscape + \footnotesize, 5-6 columns -> p{4.5cm} first col + \footnotesize + tabcolsep 4pt.
- One call -> three formats: modelsummary(models, output=".tex"/".docx"/html->xlsx) wrapped in aer_table(); gof_omit "BIC|AIC|F|Log|Adj" or gof_map (N 0 dec, R2 3 dec); fixest::etable() for fast fixest tables; gtsummary::tbl_summary(by=treat) + add_p + add_difference for Table 1.
- Anti-patterns: 14-column table, SE in two bracket styles, stars hiding magnitudes, "Notes: See text.", inconsistent decimals, dataset variable names.

### Descriptive/balance conventions [ES]
- Table 1: N, mean, SD (+ min/max/median) for all analysis variables; panel N, T, N*T; stars on differences; normalized difference Delta = (X1bar - X0bar)/sqrt(S1^2+S0^2), |Delta| < 0.25 acceptable.

### ggplot2 theme, colour, size, export [EF][ATF][GG][NF][SV][EA]
- Never ship default ggplot theme: theme_classic()/theme_minimal(base_size=...) customized; remove gridlines/borders/chartjunk; legend inside plot or below, no box.
- Fonts: sans-serif (Helvetica/Arial) or match journal body font, >= 8 pt (AER: >= 9 pt axis labels) AFTER scaling to final size; consistent family with paper.
- Line width >= 0.5 pt data, >= 0.75 pt axes. Aspect ratio not stretched.
- Size: 3.4 in (single column) or 7 in (full page) wide, height <= 9 in; set width/height in ggsave, not by resizing in LaTeX.
- Format: vector PDF/EPS for production (AER rejects raster finals for line plots); also PNG >= 300 dpi (slides/markdown); ggsave(width, height, dpi=300); opaque explicit background unless transparency needed; embed fonts (cairo_pdf).
- Colour: <= 3-4 distinguishable colours, extra series via linetype/shape; readable in grayscale; avoid red-green; viridis/cividis or Okabe-Ito/Paul Tol; never color-only encoding (add marker, linetype, direct label); sequential/diverging/qualitative per data semantics.
- Honest encoding: bars include zero baseline; points/lines may use nonzero with disclosure; log axes labelled with base; dual axes avoided (use aligned panels); area not radius; no 3D, no pie.
- Uncertainty: ALWAYS show CI/SE for estimated quantities; name the interval (SD/SE/95% CI, clustered or not), n and unit of replication; show raw observations when feasible; distinguish missing vs zero vs censored (gaps, not connected lines).
- Reference lines: zero line (coefplots), cutoff (RDD), treatment date (event study; ref period -1 stated).
- Axis labels descriptive with units; panel labels (a), (b), (c); one main claim per figure (split panels rather than overlay six lines); multi-panel panels aligned (equal plot-area widths/heights within 1.5 pt) via patchwork/cowplot.
- Figure types: event study (iplot / ggplot geom_pointrange + geom_ribbon), coefplot (modelplot / geom_pointrange; preferred over table when >= 8 specs), binscatter/binsreg, rdplot, kernel density, SCM gap + placebo plot, Bacon plot, spec curve (two-panel: sorted estimates + choice indicators).
- Figure notes (below, start "Notes:"): estimator/method, reference category, CI type and coverage, sample restrictions, N (obs or clusters), data source.
- Files: one figures/ dir, zero-padded prefixes (fig01_event_study.pdf); header comment in each script listing figures produced; never two scripts writing same file.
- Accessibility: alt text + longer description for complex figures; contrast >= 3:1 for graphical objects (WCAG 2.2: 4.5:1 text); a grayscale screen is not a full colour-vision test; check at final physical size; provenance (data path, transformations, seed) recorded.
- ggplot2 4.0 specifics [GG]: S7 objects (use `@` not `$`); theme(ink, paper, accent) and element_geom()/from_theme() for layer defaults; theme_sub_*() shortcuts; labels hierarchy aes < labs(dictionary) < column attribute < labs() < scale name < guide title; deprecations: coord_trans -> coord_transform, geom_errorbarh -> geom_errorbar(orientation="y"), fatten -> median.linewidth, draw_quantiles -> quantiles, facet_wrap(as.table) -> dir, theme_get/set -> get/set_theme, last_plot -> get_last_plot.
- Nature-style figures [NF]: write core conclusion before code; hero panel; one backend (R OR Python) per figure; render-time panel-alignment audit and collision audit after every change; verify live journal guidance (do not infer from examples).
- Journal requirements are not assumed [SV]: identify journal/article type/phase and verify live official guidance; no report certifies compliance or accessibility.

## R style

- Native pipe `|>` always (not `%>%`); R >= 4.3 / dplyr >= 1.1. [TV]
- Per-operation grouping `.by =` instead of group_by()/ungroup(); `pick()` for column selection, `across()` for apply-to-columns; `reframe()` for multi-row summaries. [TV]
- Joins: join_by(a == b); declare relationship=, unmatched="error"; na_matches="never". [TV]
- Data masking: `{{ }}` embrace for arguments; `.data[["col"]]` for strings. [TV]
- case_when(.unmatched="error") when exhaustive; replace_when() for in-place updates; filter_out(); when_any()/when_all(). [TV]
- purrr: map() |> list_rbind() (not map_dfr), walk() for side effects (writing files/plots), in_parallel() to scale; tidyr separate_wider_delim/_regex; pivot_longer/wider (not gather/spread); stringr str_ functions (string-first, vectorized). [TV]
- Serialization: qs2 for fast save (not compatible with qs). [TV]
- Names: snake_case; variables = nouns, functions = verbs; no dots except S3 methods. [RS]
- Spacing: spaces around operators, after commas; assignment `<-`; no `T`/`F` (use TRUE/FALSE); no semicolons; no extra parentheses; no attach() (use with()/explicit). [RS]
- 2-space indent, never tabs; lines < 80 chars; one argument per line for long calls. [RS]
- Comments explain WHY, not WHAT; scripts organized with header (project, date, inputs/outputs), library block top, numbered sections. [RS][DC]
- Functions: single responsibility; data-first argument; prefix non-standard args with `.`; consistent return types; defaults at the end; user errors via cli::cli_abort() with problem statement + context bullets and inline markup ({.arg x} {.fn f} {.cls} {.val} {?s}). [RS]
- Estimation idiom: feols(y ~ x | unit + year, cluster = ~unit), not lm(y ~ x + factor(unit) + factor(year)); estimators return objects passed straight to modelsummary/modelplot/etable, never hand-roll LaTeX. [EA]
- Reproducibility: renv lockfile, set.seed(), Quarto, no setwd(), relative paths, sessionInfo() in log. [EA]
- Performance: profile first (profvis for unknown bottlenecks, bench::mark for alternatives with min_iterations>=10, system.time only quick checks); profile realistic data sizes and memory. [RP]
- Never grow objects in loops: pre-allocate vector("list", n) or use map(). [TV][RP]
- Backend: data.table for >1 GB or heavy grouping; dplyr for readability / <100 MB / complex joins+windows; base R when no dependencies; fixest for HDFE regressions (fast, absorbs FE). [RP][EA]
- Do not optimize without measuring; do not trade readability for ~1% gains; do not assume loops are slow - benchmark. [RP]
- vctrs: only for package development / custom vector classes / type-stable functions; overhead for one-off analyses and tiny vectors - use base R. [RP]
- Parallel (in_parallel/future): only when per-task cost >> overhead; bootstrap/simulation loops (boottest B=9999, ri2 sims) are the typical use. [RP][EA]

## Skill index

ggplot2 | open for ggplot2 4.0 API specifics (S7 `@`, ink/paper/accent, theme_sub_*, labels dictionary, facet_wrap dir, deprecation table).
nature-figure | open for Nature-family manuscript figures: figure contract, multipanel evidence architecture, panel-alignment + PDF collision audits, AI graphical abstract policy.
scientific-visualization | open for Matplotlib/Seaborn/Plotly integrity, accessibility (WCAG), journal export planning, palette contrast audit CLIs (Python side).
econ-figure | open for econ figure code templates (event study, coefplot, binscatter, RDD, SCM gap, multi-panel) and figures/ file-naming helpers in R/Python/Stata.
econ-table | open for esttab/modelsummary/etable/stargazer templates, AER vs QJE styles, side-by-side panels, \input{} body-only and overflow fixes.
econ-stats | open for Table 1 / balance (normalized differences) / correlation / missing-data summary code.
data-cleaning | open for Stata do-file cleaning template, codebook, assert patterns (mostly Stata-centric; R version is in empirical-analysis-r).
panel-data | open for Hausman/Mundlak, Arellano-Bond GMM interpretation, Driscoll-Kraay and two-way cluster code; see references/panel-reference.md for FD, dynamic, CRE.
ols-regression | open for Gauss-Markov checklist, diagnostics table, references/ols-reference.md test formulas.
did-analysis | open for 2x2/event-study/staggered code templates; references/did-reference.md for BJS, dCDH, triple-diff, Roth power.
iv-estimation | open for 2SLS/PSM code, Wu-Hausman/Sargan table; references/iv-reference.md for AR sets, LIML, control function, Bartik, judge designs.
rdd-analysis | open for rdrobust workflow, validity-test sequence, reporting template; references/rdd-reference.md for kink, geographic, discrete running var, multi-cutoff.
synthetic-control | open for Synth/augsynth/SparseSC/synth_runner code, donor-pool guidelines, SDID, reporting list; references for staggered SCM.
time-series | open for ADF/KPSS conflict handling, ARIMA/VAR/VECM/GARCH code, Zivot-Andrews; references/time-series-reference.md for Johansen/VECM/breaks.
causal-inference-mixtape | open for cross-language (Python/R/Stata) DiD, event-study, IV, RD, SC, matching, DAG, randomization-inference templates.
empirical-analysis-r | open for full paste-runnable R pipeline (Steps -1..8), data contract, sample log, modelsummary export wrapper, HonestDiD/Oster/E-value/spec-curve code, epi + ML-causal modes; references/01-08 for depth. Huge file: read by step.
marginaleffects | open for estimands (ATE/ATT/AME), datagrid counterfactuals, hypothesis tests, robust/bootstrap uncertainty; book chapters in chapters/, man/r/.
pyfixest | open only for Python HDFE (feols/fepois/event_study/did2s/etable) API.
tidyverse-patterns | open for dplyr 1.1/1.2 idioms, join QC, purrr/stringr migration table.
r-style-guide | open for naming/spacing/function design and cli_abort error conventions.
r-performance | open for profvis/bench workflow, data.table vs dplyr choice, vctrs decisions.
aer-identification | open for decision tree and per-design required diagnostics/red flags/identification gate (DiD, IV, RDD, SCM, Bartik, RCT registry).
aer-robustness | open for referee-anticipating battery, top-5 referee comments, coverage gate, appendix structure, StatsPAI tool bindings.
aer-tables-figures | open for AER table anatomy, star/SE/decimal conventions, figure notes, pre-submission checklist; references/exhibit-cookbook.md.
phack-detection | open for p-curve battery (binomial, Fisher, Stouffer, LCM), density-jump/spike tests, phase-shift decomposition, verdict reading (Python engine).
specification-search | open for instrumented specification-universe walk, ledger/audit outputs, null schemes, pathology flags, min-p honest p-value, robustness-theatre audit.
