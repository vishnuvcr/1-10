# Reproducible Research Manuscript
## Daily 21-SMA / 14-RSI Gap-Reversion Strategy in Indian Markets

Research completion date: 23 September 2026.

## Abstract

This study evaluates a pre-specified daily mean-reversion strategy using a 21-period simple moving average and a 14-period Wilder RSI with extreme thresholds of 10 and 90. A long signal occurs when the previous session RSI is below 10 and the current session opens below the previous close. A short signal occurs when the previous session RSI is above 90 and the current session opens above the previous close. Entries are at the current open; the requested stop is the entry-candle low/high, and the take-profit is a touch/cross of the 21-SMA.

A causality audit showed that a completed entry-candle low/high is unknowable at the entry open from daily OHLC. The research therefore separates the literal requested stop from a causal daily comparison using the previous session low/high. The daily SMA target is also shifted to the prior-session SMA so that no current-close information leaks into an open-time decision.

The primary 2010-2026 NIFTY 50 sample contains 4,106 daily observations and produced no qualifying RSI<10 or RSI>90 signals. A fixed seven-symbol Indian equity universe was then tested without changing the signal thresholds. The same rule produced no trade population for several symbols and only 1-9 completed trades for symbols that did trade. A maximum-history diagnostic extending the requested start to 1990, subject to Yahoo Finance availability, produced 0 trades for NIFTY, 2 for RELIANCE, 1 for HDFCBANK, 0 for ICICIBANK, 9 for INFY, 1 for TCS, and 2 for SBIN.

Monte Carlo bootstrap analysis used 1,000 with-replacement trade-return paths where completed trades existed. Because each symbol has fewer than 30 completed trades, all inferential results are classified as descriptive-only. Four of the five trade-bearing stocks had negative final returns; TCS had one positive completed trade. Cost sensitivity showed that higher slippage and brokerage materially worsened the already sparse results.

The research does not establish a durable trading edge or production readiness for the locked rule. The strongest finding is instead an engineering and research-design conclusion: the extreme RSI thresholds create a very sparse trade population, the literal entry-bar stop is non-causal with daily data, and the empirical sample is too small for reliable robustness inference.

## 1. Introduction

Short-horizon return reversal is an established empirical theme. Jegadeesh documented negative serial dependence and predictable short-horizon behavior, while later work connected some short-horizon reversals to transaction-cost and market-microstructure effects. Bailey et al. formalized the Probability of Backtest Overfitting framework, emphasizing that repeated experimentation can create attractive but unstable historical results.

This study intentionally avoids parameter optimization in the primary experiment. The RSI thresholds 10/90, SMA period 21, entry rule, exit rule, initial capital and 1% risk budget are locked. The research question is whether that already-specified rule produces enough repeated, net-of-cost observations to support an economically meaningful conclusion.

## 2. Research Questions

1. Does the locked strategy generate a non-trivial trade population on Indian daily data?
2. Does it exhibit positive net-of-costs expectancy under a causal daily interpretation?
3. How sensitive are results to transaction costs?
4. What path variability is implied by bootstrap resampling of completed trade returns?
5. Are observed results sufficiently numerous to support inferential claims?

## 3. Aims and Objectives

Aim: build and validate a reproducible quantitative backtesting and robustness framework for the specified rule.

Objectives:
- implement chronology-safe signal generation;
- separate literal and causal execution interpretations;
- model risk-based sizing and explicit transaction costs;
- produce a complete trade ledger and equity curve;
- quantify Monte Carlo terminal-return and maximum-drawdown distributions;
- quantify drawdown-threshold probabilities;
- stress slippage and brokerage;
- quantify statistical uncertainty while respecting sample size;
- preserve raw data, hashes, code commits, results and decisions in GitHub.

## 4. Strategy Specification

Indicators:
- 21-period SMA.
- 14-period Wilder RSI.
- RSI thresholds 10 and 90.

Long:
- previous RSI < 10;
- current open < previous close;
- entry at current open;
- requested literal stop = current entry-candle low;
- causal daily comparison stop = previous session low;
- exit when price touches/crosses the prior-session 21-SMA.

Short:
- previous RSI > 90;
- current open > previous close;
- entry at current open;
- requested literal stop = current entry-candle high;
- causal daily comparison stop = previous session high;
- exit when price touches/crosses the prior-session 21-SMA.

Risk:
- starting equity INR 100,000;
- nominal risk 1% of current equity;
- quantity = floor((0.01 x equity) / absolute(entry - stop)) to lot size;
- one open position at a time.

## 5. Causality and Execution Methodology

The completed entry-candle low/high is not available at today's open. Therefore entry-bar stop sizing is non-causal on daily OHLC. The code preserves that literal mode for reproducibility and flags it as non-causal.

For causal daily execution the stop comparison uses the previous session low/high.

The target uses the previous-session 21-SMA because a current-day closing SMA is unavailable at the current open.

Daily OHLC also cannot identify intrabar ordering. The conservative policy is:
- gap-through events fill at the open;
- if stop and target are both touched later in one daily bar, stop is assumed first.

## 6. Data and Reproducibility

The prototype uses Yahoo Finance through yfinance. It is treated as a reproducible research source, not as an exchange-certified execution feed.

Primary NIFTY sample:
- date request: 2010-01-01 through 2026-09-23;
- actual first date: 2010-01-04;
- actual last date: 2026-09-21;
- rows: 4,106;
- SHA-256: 82c344b9ea3097f1ffbdb398755edbafc52f96351394397d50973fe04caa6e0a.

Maximum-history diagnostic:
| Symbol | First available date | Rows |
|---|---:|---:|
| ^NSEI | 2007-09-17 | 4,664 |
| RELIANCE.NS | 1996-01-01 | 7,713 |
| HDFCBANK.NS | 1996-01-01 | 7,716 |
| ICICIBANK.NS | 2002-07-01 | 6,018 |
| INFY.NS | 1996-01-01 | 7,716 |
| TCS.NS | 2002-08-12 | 5,989 |
| SBIN.NS | 1996-01-01 | 7,714 |

## 7. Primary NIFTY Results

| Measure | Result |
|---|---:|
| Daily observations | 4,106 |
| RSI minimum | 12.94 |
| RSI maximum | 85.60 |
| RSI < 10 observations | 0 |
| RSI > 90 observations | 0 |
| Gap-down days | 1,428 |
| Gap-up days | 2,665 |
| Long signals | 0 |
| Short signals | 0 |
| Completed trades | 0 |
| Final return | 0.00% |

This is a signal-population finding, not a profitability estimate.

## 8. Maximum-History Cross-Sectional Results

| Symbol | Trades | Final return | Max DD | Sharpe | Win rate | Expectancy per trade |
|---|---:|---:|---:|---:|---:|---:|
| ^NSEI | 0 | 0.00% | 0.00% | 0.00 |+§uçâçT | ºw^~)Þt |
| RELIANCE.NS | 2 | -4.52% | -4.52% | -0.230 | 0% | -2,235.68 |
| HDFCBANK.NS | 1 | -0.07% | -0.07% | -0.181 | 0% | -42.08 |
| ICICIBANK.NS | 0 | 0.00% | 0.00% | 0.00 |+§uçâçT | ºw^~)Þt |
| INFY.NS | 9 | -9.63% | -9.63% | -0.281 | 0% | -1,046.39 |
| TCS.NS | 1 | +5.88% | -2.26% | +0.327 | 100% | +5,900.77 |
| SBIN.NS | 2 | -2.61% | -2.61% | -0.240 | 0% | -1,283.26 |

The TCS result is based on one completed trade and cannot support a durable-edge claim.

## 9. Monte Carlo Robustness

The requested Monte Carlo used 1,000 paths, sampling completed trade returns with replacement from the observed trade-return distribution, with seed 42 and INR 100,000 starting equity.

| Symbol | Trades/path | Final return P05 | P50 | P95 | Max DD P05 | P50 | P95 | RoR >=10% | RoR >=20% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| RELIANCE.NS | 2 | -6.60% | -4.47% | -2.29% | -6.60% | -4.47% | -2.29% | 0% | 0% |
| HDFCBANK.NS | 1 | -0.04% | -0.04% | -0.04% | -0.04% | -0.04% | -0.04% | 0% | 0% |
| INFY.NS | 9 | -18.78% | -9.19% | -2.70% | -18.78% | -9.19% | -2.70% | 41.0% | 1.9% |
| TCS.NS | 1 | +5.90% | +5.90% | +5.90% | 0% | 0% | 0% | 0% | 0% |
| SBIN.NS | 2 | -3.52% | -2.57% | -1.60% | -3.52% | -2.57% | -1.60% | 0% | 0% |

All 30/40/50% drawdown probabilities were zero in this very small empirical sample. That does not imply true low tail risk; with one or two observed trades the bootstrap support is nearly degenerate.

Plots:
- results/history_extension/RELIANCE.NS/monte_carlo_equity_curves.png
- results/history_extension/HDFCBANK.NS/monte_carlo_equity_curves.png
- results/history_extension/INFY.NS/monte_carlo_equity_curves.png
- results/history_extension/TCS.NS/monte_carlo_equity_curves.png
- results/history_extension/SBIN.NS/monte_carlo_equity_curves.png

## 10. Cost Sensitivity

Fixed grid:
- slippage 0, 5, 10, 20 bps;
- brokerage INR 0, 20, 40 per order;
- all signal parameters unchanged.

Baseline versus stress:

| Symbol | Baseline return | Stress return |
|---|---:|---:|
| ^NSEI | 0.00% | 0.00% |
| RELIANCE.NS | -4.52% | -14.83% |
| HDFCBANK.NS | -0.07% | -0.17% |
| ICICIBANK.NS | 0.00% | 0.00% |
| INFY.NS | -9.63% | -28.33% |
| TCS.NS | +5.88% | +5.78% |
| SBIN.NS | -2.61% | -7.20% |

The cost surface is consistent with a friction-sensitive strategy, but the small samples prevent a robustness claim.

## 11. Statistical Validation

Bootstrap mean-return confidence intervals used 10,000 resamples. Exact two-sided binomial sign tests used p=0.5.

| Symbol | n | Mean return | 95% bootstrap CI | P(bootstrap mean > 0) | Sign-test p |
|---|---:|---:|---:|---:|---:|
| RELIANCE.NS | 2 | -2.26% | [-3.36%, -1.15%] | 0.000 | 0.5000 |
| HDFCBANK.NS | 1 | -0.04% | [-0.04%, -0.04%] | 0.000 | 1.0000 |
| INFY.NS | 9 | -1.08% | [-2.37%, -0.22%] | 0.000 | 0.0039 |
| TCS.NS | 1 | +5.90% | [+5.90%, +5.90%] | 1.000 | 1.0000 |
| SBIN.NS | 2 | -1.29% | [-1.78%, -0.80%] | 0.000 | 0.5000 |

Every symbol is classified as descriptive-only because n < 30.

Across all 15 completed trades, the pooled descriptive mean trade return was -0.729% and the median was -0.804%. Cross-sectional independence is not assumed.

DSR and PBO are not asserted because no parameter-selection tournament was conducted in this study.

## 12. Discussion

The main empirical finding is the lack of observations. The locked RSI thresholds are so extreme that NIFTY has no qualifying observations in the primary 2010-2026 sample and the maximum-history equity tests remain extremely sparse.

This makes standard metrics unstable. A single positive TCS trade creates a positive result but no statistical basis for generalization. Nine losing INFY trades provide more information than one trade, but the sample is still far too small for a stable population estimate.

The causality audit is equally important. A daily backtest must not use the completed entry candle's low/high to size a position at that same bar's open. The project therefore provides both the literal user specification and a causal previous-bar comparison.

Transaction-cost stress shows why the cost model must stay explicit. Short-horizon reversal strategies can be highly sensitive to execution friction.

Monte Carlo analysis is useful here as a risk-engineering and implementation check, but not as a magic generator of information. Resampling two observed outcomes still leaves only two outcomes in the empirical support.

## 13. Strengths

- locked parameters before primary interpretation;
- chronology-safe target definition;
- explicit causal and non-causal stop modes;
- parameterized transaction costs;
- deterministic same-day conflict policy;
- frozen raw data and SHA-256 manifests;
- reproducible GitHub Actions execution;
- complete trade/equity/Monte Carlo artifacts;
- error log preserving implementation mistakes and fixes.

## 14. Limitations

- Yahoo Finance is not an exchange-certified execution dataset;
- daily OHLC cannot reconstruct true intrabar order;
- literal entry-bar stop remains non-causal;
- stock short-side economics are not equivalent to index/futures execution;
- the maximum symbol-level trade count is 9;
- cross-sectional pooling is descriptive;
- no live/paper-trading evidence;
- execution-grade corporate-action/tradability reconciliation remains future work.

## 15. Conclusion

The locked daily 21-SMA / 14-RSI 10/90 gap-reversion strategy does not generate enough observations in the tested Indian-market universe to support a credible durable-edge claim.

The NIFTY 50 primary sample generated zero qualifying signals. The maximum-history diagnostic generated only 15 completed trades across the five symbols that traded at all. Four symbols ended negative; TCS had one positive trade. Costs worsened results materially for most negative cases. Statistical validation correctly classifies all symbol-level evidence as descriptive-only.

The research therefore stops here rather than changing the thresholds to manufacture activity. The repository now contains the complete reproducible backtesting, Monte Carlo, cost-sensitivity and statistical-validation framework.

No production or live-trading strategy is promoted from this evidence.

## 16. Future Research

1. Use intraday data if the literal entry-candle low/high stop is required.
2. Move to a directly tradable instrument with exchange-accurate lot size, margin/borrow and statutory costs.
3. Pre-register any broader RSI threshold variants as new experiments rather than modifying this result.
4. Test volatility/regime conditioning with India VIX, breadth and trend-state variables.
5. Use walk-forward, purged validation and formal multiple-testing controls once sufficient trade counts exist.
6. Maintain the repository's frozen-data and error-log discipline.

## Appendix A - Monte Carlo

For trade return r_t, path equity is E_t = E_(t-1) x (1 + r_t), with E_0 = INR 100,000.

Maximum drawdown is the minimum of E_t / running_peak_t - 1.

Risk of ruin at drawdown threshold q is the fraction of simulated paths whose maximum drawdown is <= -q.

## Appendix B - Reproducibility Contract

For every published result record:
- Git SHA;
- Python/package versions;
- ticker;
- exact date range;
- raw-data path and SHA-256;
- strategy parameters;
- stop mode;
- target definition;
- cost assumptions;
- Monte Carlo seed and count;
- complete trade ledger;
- equity curve.

## Appendix C - Repository Map

- backtest.py: primary engine.
- requirements.txt: dependency specification.
- tests/test_backtest.py: unit tests.
- docs/RESEARCH_PLAN.md: research protocol.
- docs/LITERATURE_MATRIX.md: literature review.
- docs/DATA_SOURCE_REGISTRY.md: data-source hierarchy.
- docs/ERROR_LOG.md: implementation error history.
- docs/VALIDATION_LOG.md: validation history.
- results/history_extension: maximum-history empirical results.
- results/cost_sensitivity.csv: 84-run cost grid.
- results/statistical_validation.csv: bootstrap and sign-test summary.

## Appendix D - Literature

Jegadeesh, N. (1990). Evidence of Predictable Behavior of Security Returns. Journal of Finance, 45(3), 881-898. DOI 10.1111/j.1540-6261.1990.tb05110.x.

Jegadeesh, N. and Titman, S. (1990). Short Horizon Reversals and the Bid-Ask Spread.

Bailey, D. H., Borwein, J. M., Lopez de Prado, M. and Zhu, Q. J. (2017). The Probability of Backtest Overfitting. Journal of Computational Finance, 20(4), 39-69. DOI 10.21314/JCF.2016.322.

The repository literature matrix records additional 2026 Indian-market technical-rule preprints and source-audit notes.
