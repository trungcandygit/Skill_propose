# Methods with no ready-made skill (written for this playbook)

No vetted skill was found for these topics. This file was written from standard methodology (textbooks and package documentation as generally known), not copied from a skill. Treat thresholds as conventions that journals and advisors may override, and check function names against the installed package version before running code.

Contents: A. Survey scales, EFA, CFA, PLS-SEM. B. Dynamic panel GMM. C. Quantile regression. D. Event study and asset-pricing tests. E. Valuation. F. Vietnamese and ASEAN data. G. Bayesian regression. H. What to report for every method.

## A. Survey scales, EFA, CFA, PLS-SEM

Order of work: design the questionnaire, pilot, clean (missing data, straight-lining, attention checks), then measurement validity, then structural model.

**Scale reliability and EFA**
- Cronbach's alpha: >= 0.70 is the usual floor; very high (> 0.95) suggests redundant items. Report alpha per construct and "alpha if item deleted".
- Before EFA: KMO >= 0.60 (>= 0.80 good), Bartlett's test of sphericity significant, sample size at least 5 to 10 respondents per item and not below about 100.
- Extraction and rotation: principal axis or ML for common factors; oblique rotation (oblimin or promax) when factors may correlate, varimax only when theory says orthogonal. Decide factor count with parallel analysis plus theory, not the eigenvalue > 1 rule alone.
- Retain loadings >= 0.50 (or >= 0.40 with justification), delete items with cross-loadings within about 0.15 of the primary loading, one deletion at a time, rerun after each.
- R: `psych::KMO`, `psych::cortest.bartlett`, `psych::fa.parallel`, `psych::fa`, `psych::alpha`. Report the table of loadings, communalities, variance explained.

**CFA / CB-SEM** (testing a theory)
- R: `lavaan::cfa`, `lavaan::sem`. Report chi-square with df, CFI and TLI >= 0.90 (>= 0.95 good), RMSEA <= 0.08 (<= 0.06 good), SRMR <= 0.08. Convergent validity: AVE >= 0.50, composite reliability >= 0.70. Discriminant validity: Fornell-Larcker or HTMT (< 0.85 strict, < 0.90 lenient).
- Do not modify the model with modification indices without theoretical reasons; say so if you did.

**PLS-SEM** (prediction and theory development, small samples, formative constructs)
- Software: SmartPLS 4 or R `seminr`. Choose PLS-SEM over CB-SEM when the goal is prediction or exploration, not strict model fit.
- Measurement model (reflective): indicator loadings >= 0.708 (0.40 to 0.70 case by case), Cronbach alpha and rho_A and CR between 0.70 and 0.95, AVE >= 0.50, discriminant validity by HTMT (< 0.90, and bootstrap CI not containing 1).
- Measurement model (formative): check collinearity (VIF < 3, at most < 5), outer weights significance and relevance, redundancy analysis.
- Structural model: VIF of predictors, path coefficients with bootstrap (5,000 resamples, report t, p, and percentile or BCa CIs), R-squared (0.25, 0.50, 0.75 weak, moderate, substantial in the common rule of thumb), f-squared (0.02, 0.15, 0.35), Q-squared predict, and PLSpredict (compare to a linear model benchmark).
- Mediation: bootstrap the indirect effect; classify as full, partial, or none. Moderation: product-indicator or two-stage; plot simple slopes.
- Common-method bias: Harman's single factor is weak; prefer a full-collinearity VIF check (< 3.3) and procedural remedies.
- Sample size: use G*Power or the inverse square root method; state it.

## B. Dynamic panel GMM (difference and system)

- Use when the model includes a lagged dependent variable, regressors are endogenous, N is large and T is small. With T large and N small, GMM instruments proliferate; consider other estimators.
- Stata `xtabond2` (Roodman) or R `plm::pgmm`, `pdynmc`. Declare which variables are treated as endogenous, predetermined, or strictly exogenous, and which instrument lags are used (restrict the lag range, collapse the instrument matrix).
- Always report: number of observations, groups, number of instruments (should not exceed the number of groups), AR(1) significant and AR(2) insignificant in first differences, Hansen J (p between about 0.10 and 0.90, p very close to 1.00 signals instrument proliferation), difference-in-Hansen for the system-GMM level instruments, and whether the two-step estimator uses Windmeijer-corrected standard errors.
- Robustness: compare with pooled OLS and fixed effects as bounds for the lagged-dependent coefficient (the GMM estimate should lie between the FE and OLS estimates), vary the lag range, collapse or not, one-step vs two-step.
- Do not describe GMM as proving causality; say what exogeneity assumptions the instruments rely on.

## C. Quantile regression

- Purpose: effects that differ across the conditional distribution (for example, firm performance for low vs high performers).
- R: `quantreg::rq`; standard errors by bootstrap (`se = "boot"`, pairs or cluster bootstrap with at least 1,000 replications) especially with heteroskedasticity or clusters. Panel data with fixed effects needs a dedicated method (for example `rqpd`, Canay two-step, or method of moments quantile regression, MMQR in Stata `xtqreg`); state which and why.
- Report coefficients at a grid of quantiles (for example 0.10, 0.25, 0.50, 0.75, 0.90), a figure of coefficients with confidence bands against OLS, and a test of equality across quantiles (`anova.rq`).
- Avoid quantile crossing problems by rearrangement and say so if it occurs.

## D. Event study and asset-pricing tests

**Event study (short window)**
- Define event date and estimation window (for example [-250, -30] before the event), event windows (for example [-1,+1], [-5,+5]), market model or Fama-French factor model for expected returns.
- Abnormal returns AR, cumulative CAR; test with the cross-sectional t-test plus a robust one (BMP standardized test, Kolari-Pynnonen when events cluster in time), and a non-parametric test (sign or rank test).
- Check: overlapping events and event clustering, thin trading and non-synchronous trading (important for small markets), confounding events, outliers (winsorize). Show the CAR path figure with confidence bands.

**Long-horizon and factor models**
- CAPM, Fama-French three or five factor, plus momentum: time-series alpha tests with GRS; cross-sectional tests with Fama-MacBeth (report Newey-West adjusted t-statistics, and the Shanken correction when betas are estimated).
- Portfolio sorts: univariate and bivariate sorts, value-weighted and equal-weighted, long-short spread with Newey-West t-statistics. Avoid look-ahead bias (lag accounting data at least 3 to 6 months).
- Factor data for non-US markets must come from a local construction or a clearly cited source; do not reuse US factors for Vietnam without saying so.

## E. Valuation (company and equity)

- DCF: free cash flow to firm, WACC from CAPM (state risk-free rate, equity risk premium, beta source, country risk), terminal value by growth or exit multiple, sensitivity table over WACC and terminal growth. Show that terminal value share of EV is not excessive.
- Relative valuation: comparable multiples (P/E, EV/EBITDA, P/B) with a defensible peer set and median not mean; adjust for size, growth, leverage.
- Residual income and dividend discount models for banks and financials where FCF is ill-defined.
- Report model uncertainty (scenario or Monte Carlo ranges), data cut-off date, and reconcile with market price. Use the bundled `skills/fin-quantitative-valuation/`, `skills/fin-company-valuation/`, `skills/fin-dcf-model/`.

## F. Vietnamese and ASEAN data

- Market data: Python `vnstock` (check the installed version's documentation; its API has changed between versions), exchange websites (HOSE, HNX), SSC disclosures. Always record data source, retrieval date, and adjustment for splits, dividends and bonus shares (price adjustment errors are a common source of false returns).
- Financial statements: company filings and data vendors; align fiscal year ends, treat banks separately from non-financial firms, and use consistent consolidated vs parent-only statements.
- Thin trading and price limits (daily limits on HOSE and HNX) distort returns: use Dimson or Scholes-Williams betas or longer windows, and report the share of zero-return days.
- Macro data: GSO (Vietnam General Statistics Office), State Bank of Vietnam, IMF, World Bank, ADB. Keep a data-source table (variable, definition, source, frequency, period) in the appendix.
- Cross-country panels (ASEAN-6 etc.): harmonise definitions and currency units, deflate by CPI to a base year, and cluster at the country or firm level as appropriate.
- Optional tooling: `skills/fin-api-data-fetcher/`, `skills/toolkit-data-fetcher/`, `skills/fin-edgartools/` (US SEC filings only), `skills/soc-data-finder/`.

## G. Bayesian regression

- Use when priors are informative, samples are small, hierarchical structure matters, or full posterior uncertainty is wanted.
- Workflow: write the model and priors, prior predictive check, sample (PyMC or `brms`), diagnostics (R-hat <= 1.01, effective sample size, divergences, trace plots), posterior predictive check, prior sensitivity, report posterior means and 94 or 95 percent credible intervals, not p-values. Use `skills/bayes-bayesian-workflow/`, `skills/stat-pymc/`, `skills/bayes-causal-inference/`.
- Say clearly which statements are Bayesian credible intervals and avoid mixing them with frequentist language.

## H. What to report for every method

Estimator and software with version; sample, N and clusters; the identifying or modelling assumption in one sentence; diagnostics run and their results; robustness checks (at least three that probe the assumption); effect size with uncertainty, not only significance; limitations stated in plain words. This list feeds the panel check in `references/panel-protocol.md`.
