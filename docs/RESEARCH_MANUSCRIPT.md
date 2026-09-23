# Reproducible Research Manuscript
## Daily 21-SMA / 14-RSI Gap-Reversion Strategy in Indian Markets

**Research completion date:** 23 September 2026  
**Repository:** vishnuvcr/1-10  
**Final research branch:** phase-7-manuscript

---

## Abstract

This study evaluates a pre-specified daily mean-reversion strategy using a 21-period simple moving average (SMA) and a 14-period Wilder relative-strength index (RSI). A long signal requires previous-session RSI < 10 and the current open below the previous close; a short signal requires previous-session RSI > 90 and the current open above the previous close. The strategy starts with INR 100,000 and targets a nominal 1% equity risk per trade.

A chronology audit found that the requested entry-candle low/high stop is not observable at the entry open when only daily OHLC data are available. The implementation therefore preserves the literal requested mode for auditability but separately defines a causal daily comparison using the previous session's low/high. The daily SMA target is also based on the prior-session 21-SMA to avoid current-day close leakage.

The primary NIFTY 50 sample contains 4,106 daily observations from 2010-01-04 through 2026-09-21 and produces zero qualifying signals under the locked RSI 10/90 thresholds. A fixed seven-symbol Indian equity universe is then evaluated with unchanged signal parameters. Extending the same rule to the maximum Yahoo Finance history available for the selected symbols produces only 15 completed trades in total: 0 for NIFTY, 2 for RELIANCE, 1 for HDFCBANK, 0 for ICICIBANK, 9 for INFY, 1 for TCS, and 2 for SBIN.

The 1,000-path trade bootstrap is therefore informative mainly as a risk-engineering check, not as a reliable population estimator. Cost sensitivity over 84 fixed combinations shows worsening performance with increased slippage and brokerage for every trade-bearing negative case. Statistical validation uses 10,000 non-parametric bootstrap resamples of mean trade return and exact binomial sign tests; every symbol remains below a 30-trade threshold and is classified as descriptive-only.

The study does not establish a durable trading edge or production readiness. Its primary contribution is a reproducible research framework and an empirical finding that the locked rule is too sparse, with daily execution limitations that prevent a credible robustness claim.

---

## 1. Introduction

Short-horizon return reversal is a long-standing empirical research topic. Jegadeesh (1990) documented negative serial correlation in short-horizon stock returns and related predictability in historical US data. Lehmann (1990) reported short-horizon winner/loser reversals and discussed liquidity and transaction-cost interpretations. Jegadeesh and Titman (1990) connected short-horizon negative serial covariance to inventory-based market-microstructure mechanisms.

These findings motivate testing reversal hypotheses, but they do not validate any particular RSI/gap rule or transfer directly across markets, instruments, or eras. The present study therefore treats the rule as a fixed hypothesis rather than as an assumed anomaly.

Backtest overfitting is a second methodological concern. White's Reality Check formalized the data-snooping problem when the same historical sample is reused across candidate rules. Bailey et al. developed the Probability of Backtest Overfitting framework, and Bailey and LÛpez de Prado developed the Deflated Sharpe Ratio for selection bias and non-normality. Because this project deliberately avoided a parameter-selection tournament, it does not claim a DSR or PBO estimate; instead, it keeps the primary parameters locked and reports the severe trade-count limitation explicitly.

---

## 2. Research Questions

1. Does the locked strategy generate a non-trivial trade population on Indian daily data?
2. Does it exhibit positive net-of-costs expectancy under a causal daily interpretation?
3. How sensitive are results to slippage and brokerage?
4. What variability is implied by bootstrap resampling of the completed trades?
5. Are the observed results numerous enough to support inferential claims?

---

## 3. Aim and Objectives

### Aim

To develop and validate a chronology-safe, reproducible backtesting and robustness framework for the specified 21-SMA / 14-RSI gap-reversion rule.

### Objectives

- implement the signal chronology without future-price leakage;
- preserve both literal and causal stop interpretations;
- implement equity-based position sizing;
- model explicit execution friction;
- generate complete trade ledgers and equity curves;
- quantify bootstrap terminal-return and drawdown distributions;
- stress slippage and brokerage;
- quantify statistical uncertainty without overstating tiny samples;
- freeze data, code, hashes, decisions and errors in Git.

---

## 4. Locked Strategy Specification

### Indicators

- SMA: 21 periods.
- RSI: 14 periods using Wilder-style smoothing.
- Long threshold: previous RSI < 10.
- Short threshold: previous RSI > 90.

### Long

- previous RSI < 10;
- current open < previous close;
- entry at current open;
- requested literal stop = current entry-candle low;
- causal daily stop = previous session low;
- target = prior-session 21-SMA.

### Short

- previous RSI > 90;
- current open > previous close;
- entry at current open;
- requested literal stop = current entry-candle high;
- causal daily stop = previous session high;
- target = prior-session 21-SMA.

### Risk and capital

- starting equity: INR 100,000;
- nominal risk budget: 1% of current equity;
- one open position at a time;
- quantity rounded down to the lot size.

---

## 5. Scientific Methodology

### 5.1 Chronology and causality

The requested entry-candle low/high is not known at the opening price at which the position is entered. Using it for same-bar position sizing would therefore introduce look-ahead bias.

The project preserves the requested mode as `entry_bar_extreme` but flags it as non-causal. The main daily research interpretation uses `previous_bar_extreme`.

The exit target is the previous-session SMA rather than a current-day closing SMA because the current day has not yet closed at entry time.

### 5.2 Daily OHLC ambiguity

Daily bars do not identify the intrabar order when both stop and target are touched. The implementation uses a deterministic conservative rule:

- a gap through a stop or target is filled at the open;
- when both are touched later in the same daily bar, the stop is assumed first.

This policy is documented rather than inferred after observing results.

### 5.3 Position sizing

The nominal quantity is:

[
Q = leftlfloorrac{0.01E}{|P_{entry}-P_{stop}|}ightfloor
]

where (E) is current equity.

The actual traded quantity is rounded down to the requested lot size.

### 5.4 Transaction costs

The cost model exposes:

- slippage in basis points;
- fixed brokerage per order;
- exchange turnover charges;
- STT;
- stamp duty;
- GST on modeled brokerage/exchange/SEBI components;
- SEBI turnover charges.

The primary run uses 5 bps slippage and INR 20 brokerage per executed order, with the remaining instrument-specific statutory rates parameterized. These values are a research configuration, not a claim about a broker's current tariff for every segment.

### 5.5 Monte Carlo

When completed trades exist, 1,000 paths are created by sampling observed trade returns with replacement. Starting equity is INR 100,000 and the random seed is 42.

The bootstrap estimates:

- final-return percentiles;
- maximum-drawdown percentiles;
- probability of reaching specified peak-to-trough drawdown levels.

Because bootstrap support is limited to observed trades, one- and two-trade samples produce nearly degenerate distributions and cannot establish population tail behavior.

---

## 6. Data Sources and Provenance

### Primary prototype source

Yahoo Finance via yfinance was used for reproducible acquisition. It is treated as a convenience research source and not an exchange-certified order/execution record.

### Exchange/source hierarchy

For future execution-grade work, the repository's data-source registry prioritizes:

1. NSE official historical equity/index/derivatives data;
2. exchange/regulatory participant and settlement publications;
3. RBI/SEBI primary series where required;
4. yfinance and public GitHub/Kaggle datasets only as reproducibility or cross-check sources.

### Primary NIFTY dataset

- requested range: 2010-01-01 through 2026-09-23;
- actual first trading date: 2010-01-04;
- actual last date in downloaded sample: 2026-09-21;
- observations: 4,106;
- frozen SHA-256: `82c344b9ea3097f1ffbdb398755edbafc52f96351394397d50973fe04caa6e0a`.

### Maximum-history diagnostic

| Symbol | First available date | Rows |
|---|---:|---:|
| ^NSEI | 2007-09-17 | 4,664 |
| RELIANCE.NS | 1996-01-01 | 7,713 |
| HDFCBANK.NS | 1996-01-01 | 7,716 |
| ICICIBANK.NS | 2002-07-01 | 6,018 |
| INFY.NS | 1996-01-01 | 7,716 |
| TCS.NS | 2002-08-12 | 5,989 |
| SBIN.NS | 1996-01-01 | 7,714 |

Every frozen file has a recorded SHA-256 in its backtest manifest.

---

## 7. Phase 2 Primary NIFTY Results

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

This is a **signal-population finding**, not an estimate of strategy profitability.

---

## 8. Cross-Sectional Maximum-History Results

| Symbol | Trades | Final return | Max DD | Sharpe | Win rate | Expectancy/trade |
|---|---:|---:|---:|---:|---:|---:|
| ^NSEI | 0 | 0.00% | 0.00% | 0.000 | N/A | N/A |
| RELIANCE.NS | 2 | -4.52% | -4.52% | -0.230 | 0% | -2,235.68 |
| HDFCBANK.NS | 1 | -0.07% | -0.07% | -0.181 | 0% | -42.08 |
| ICICIBANK.NS | 0 | 0.00% | 0.00% | 0.000 | N/A | N/A |
| INFY.NS | 9 | -9.63% | -9.63% | -0.281 | 0% | -1,046.39 |
| TCS.NS | 1 | +5.88% | -2.26% | +0.327 | 100% | +5,900.77 |
| SBIN.NS | 2 | -2.61% | -2.61% | -0.240 | 0% | -1,283.26 |

The TCS result is based on one completed trade and is therefore not evidence of a stable effect.

Across the five trade-bearing symbols, only 15 completed trades were available.

---

## 9. Monte Carlo Robustness Results

| Symbol | Trades/path | Final P05 | Final P50 | Final P95 | Max DD P05 | Max DD P50 | Max DD P95 | RoR >=10% | RoR >=20% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| RELIANCE.NS | 2 | -6.60% | -4.47% | -2.29% | -6.60% | -4.47% | -2.29% | 0% | 0% |
| HDFCBANK.NS | 1 | -0.04% | -0.04% | -0.04% | -0.04% | -0.04% | -0.04% | 0% | 0% |
| INFY.NS | 9 | -18.78% | -9.19% | -2.70% | -18.78% | -9.19% | -2.70% | 41.0% | 1.9% |
| TCS.NS | 1 | +5.90% | +5.90% | +5.90% | 0.00% | 0.00% | 0.00% | 0% | 0% |
| SBIN.NS | 2 | -3.52% | -2.57% | -1.60% | -3.52% | -2.57% | -1.60% | 0% | 0% |

The observed risk-of-ruin numbers must not be interpreted as true long-run probabilities when the empirical support contains only 1-9 trades.

### Figures

Frozen Monte Carlo equity-curve figures are stored under:

- `results/history_extension/RELIANCE.NS/monte_carlo_equity_curves.png`
- `results/history_extension/HDFCBANK.NS/monte_carlo_equity_curves.png`
- `results/history_extension/INFY.NS/monte_carlo_equity_curves.png`
- `results/history_extension/TCS.NS/monte_carlo_equity_curves.png`
- `results/history_extension/SBIN.NS/monte_carlo_equity_curves.png`

---

## 10. Cost Sensitivity

An 84-combination fixed grid was evaluated:

- slippage: 0, 5, 10, 20 bps;
- brokerage: INR 0, 20, 40 per order;
- signal rules unchanged.

### Baseline vs stress

| Symbol | Baseline return (5 bps, INR20) | Stress return (20 bps, INR40) |
|---|---:|---:|
| ^NSEI | 0.00% | 0.00% |
| RELIANCE.NS | -4.52% | -14.83% |
| HDFCBANK.NS | -0.07% | -0.17% |
| ICICIBANK.NS | 0.00% | 0.00% |
| INFY.NS | -9.63% | -28.33% |
| TCS.NS | +5.88% | +5.78% |
| SBIN.NS | -2.61% | -7.20% |

The direction of the cost effect is consistent: higher trading friction worsens the negative outcomes and reduces the single positive TCS result. The small trade counts prevent a statistical robustness claim.

---

## 11. Statistical Validation

### Methods

- 10,000 non-parametric bootstrap samples for the mean trade return;
- 95% percentile intervals;
- exact two-sided binomial sign tests for a 50% positive-trade null;
- all symbol-level results with (n<30) explicitly labeled descriptive-only.

### Results

| Symbol | n | Mean trade return | 95% bootstrap CI | P(mean > 0) by bootstrap | Sign-test p |
|---|---:|---:|---:|---:|---:|
| RELIANCE.NS | 2 | -2.26% | [-3.36%, -1.15%] | 0.000 | 0.5000 |
| HDFCBANK.NS | 1 | -0.04% | [-0.04%, -0.04%] | 0.000 | 1.0000 |
| INFY.NS | 9 | -1.08% | [-2.37%, -0.22%] | 0.000 | 0.0039 |
| TCS.NS | 1 | +5.90% | [+5.90%, +5.90%] | 1.000 | 1.0000 |
| SBIN.NS | 2 | -1.29% | [-1.78%, -0.80%] | 0.000 | 0.5000 |

Across the 15 completed trades, pooled descriptive mean trade return was -0.729% and the pooled median was -0.804%.

The pooled view is descriptive only; symbol-level dependence, overlapping market regimes and different listing histories mean the 15 trades should not be treated as 15 independent experiments.

Because the study did not run a parameter-selection tournament, Deflated Sharpe Ratio and Probability of Backtest Overfitting are not asserted as numerical findings.

---

## 12. Discussion

### 12.1 Signal scarcity dominates the inference problem

The clearest empirical finding is that the locked RSI thresholds are extremely selective. NIFTY's primary sample has no RSI observations below 10 or above 90, and the fixed cross-sectional universe produces only a handful of qualifying observations even when the history is extended to the earliest Yahoo Finance dates available for each symbol.

This means the strategy is not merely showing a weak average result; it is failing to generate enough independent trade observations for normal backtest inference.

### 12.2 The one-trade positive result is not durable evidence

TCS produces a +5.88% final return from one completed trade under the baseline cost model. That outcome is reproducible within the frozen dataset, but one trade cannot support a population-level claim.

### 12.3 Negative observations dominate the available trade population

RELIANCE, HDFCBANK, INFY and SBIN all have negative final returns. INFY has the largest trade count at 9, but even that is below the predefined 30-trade threshold for inferential treatment.

### 12.4 Costs matter in the direction expected for a short-horizon reversal rule

The fixed cost grid shows that increasing slippage and brokerage reduces returns for the trade-bearing negative cases. The result is methodologically important because a frictionless backtest could materially understate implementation drag.

### 12.5 Daily data impose a structural execution limitation

The user-requested entry-bar stop is not observable at the entry open when only daily OHLC is available. An intraday feed is therefore necessary if the literal stop is to be tested faithfully. This is a data-resolution problem, not a minor implementation preference.

### 12.6 Why no further parameter search was performed

Changing RSI thresholds, SMA length, gap definition or stop logic after observing the sparse/negative result would create a new research question and introduce selection risk. Consistent with the preregistered plan, the study stops rather than optimizing toward activity or return.

---

## 13. Strengths

1. Parameters were locked before the primary empirical interpretation.
2. Current-bar SMA leakage was removed.
3. Literal and causal stop modes were separated.
4. Same-day OHLC ambiguity was handled by a deterministic conservative policy.
5. Costs were explicit and stress-tested.
6. Raw-data SHA-256 values and code SHAs were recorded.
7. CI executed the same code used to generate the saved artifacts.
8. Errors and implementation fixes were preserved in the repository.
9. Monte Carlo and statistical procedures were deterministic through stored seeds.
10. The study stopped at a pre-defined phase boundary rather than optimizing after seeing results.

---

## 14. Limitations

- Yahoo Finance is not an exchange-certified execution source.
- Daily OHLC cannot reconstruct intrabar price order.
- The literal entry-bar stop remains non-causal.
- Stock short-side financing/borrow mechanics are not modeled as an execution-grade short-selling study.
- Exact broker-specific statutory charges were not treated as universal constants; they remain configurable.
- Corporate-action/tradability reconciliation is not yet exchange-grade for every equity history.
- The largest symbol-level trade count is 9.
- Cross-sectional pooling is descriptive rather than an independence-based estimator.
- No live or paper-trading validation was conducted.
- The study does not establish performance outside the frozen datasets and execution assumptions.

---

## 15. Conclusion

The locked 21-SMA / 14-RSI 10/90 gap-reversion rule does not generate enough observations in the tested Indian-market datasets to support a credible durable-edge claim.

The primary NIFTY 50 sample generated zero qualifying signals. The maximum-history diagnostic generated only 15 completed trades across the five symbols that traded at all. Four of those five symbols had negative final returns; the remaining positive outcome came from one TCS trade. Cost stress generally worsened the negative results. Every symbol remains below the predefined 30-trade inference threshold.

The most defensible conclusion is therefore methodological and empirical: **the rule is too sparse for reliable robustness inference under the tested daily data and execution model**. The study does not promote the rule to live or production trading.

The research stops here by design. Any change to RSI thresholds, SMA period, gap definition, stop construction, regime filtering, instrument universe or execution resolution should begin as a new preregistered experiment rather than modifying this result.

---

## 16. Future Research Directions

1. Acquire exchange-quality intraday data and reconstruct the literal entry-candle stop.
2. Evaluate a directly tradable instrument with exchange-accurate lot size, margin, borrow and statutory charges.
3. Pre-register any threshold variants before rerunning history.
4. Add regime conditioning using volatility, breadth and trend-state variables only as a new hypothesis.
5. Incorporate option-chain, FII/DII, India VIX and other market-state variables only after the base rule has a sufficient trade population.
6. Use walk-forward and purged validation once a larger sample exists.
7. Apply White's Reality Check, PBO/CSCV and DSR only when a genuine family of candidate strategies has been explored.
8. Revisit the question on a longer, exchange-certified dataset if trade sparsity remains the central result.

---

## Appendix A+ßuÁ‚ùÁT Equations

Position size:

[
Q = leftlfloorrac{0.01E}{|P_{entry}-P_{stop}|}ightfloor
]

Trade-return compounding:

[
E_t = E_{t-1}(1+r_t)
]

Maximum drawdown:

[
DD_t = rac{E_t}{max_{sle t}E_s}-1
]

Risk-of-ruin at threshold (q):

[
RoR(q)=rac{1}{N}sum_{i=1}^{N}I(DD_i^{max}le -q)
]

---

## Appendix B ∫w^~)ﬁt Frozen Repository Artifacts

- `results/history_extension/*/backtest_metrics.json`
- `results/history_extension/*/trades.csv`
- `results/history_extension/*/equity_curve.csv`
- `results/history_extension/*/monte_carlo_summary.json`
- `results/history_extension/*/monte_carlo_distribution.csv`
- `results/history_extension/*/monte_carlo_equity_curves.png`
- `results/cost_sensitivity.csv`
- `results/cost_sensitivity_baseline_vs_stress.csv`
- `results/statistical_validation.csv`
- `results/statistical_validation_pooled.json`

---

## Appendix C+ßuÁ‚ùÁT Literature

1. Jegadeesh, N. (1990). *Evidence of Predictable Behavior of Security Returns*. The Journal of Finance, 45(3), 881-898. DOI: 10.1111/j.1540-6261.1990.tb05110.x.
2. Lehmann, B. N. (1990). *Fads, Martingales, and Market Efficiency*. The Quarterly Journal of Economics, 105(1), 1-28. DOI: 10.2307/2937816.
3. Jegadeesh, N. and Titman, S. (1990). *Short Horizon Reversals and the Bid-Ask Spread*.
4. White, H. (2000). *A Reality Check for Data Snooping*. Econometrica, 68(5), 1097-1126. DOI: 10.1111/1468-0262.00152.
5. Bailey, D. H., Borwein, J. M., LÛpez de Prado, M. and Zhu, Q. J. (2017). *The Probability of Backtest Overfitting*. Journal of Computational Finance, 20(4), 39-69. DOI: 10.21314/JCF.2016.322.
6. Bailey, D. H. and LÛpez de Prado, M. (2014). *The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality*. Journal of Portfolio Management, 40(5), 94-107. DOI: 10.2139/ssrn.2460551.
7. Pillai, S. (2026). *Technical-Indicator Strategy Performance in Indian Equities: A Joint Test of Market Efficiency, 2015-2025*. Working paper/preprint; included as contextual Indian-market evidence, not as validation of the present rule.

---

## Appendix D ∫w^~)ﬁt Repository Map

- `backtest.py`: primary event-driven backtest engine.
- `tests/test_backtest.py`: seven unit tests.
- `docs/RESEARCH_PLAN.md`: locked research protocol.
- `docs/LITERATURE_MATRIX.md`: literature review and source notes.
- `docs/DATA_SOURCE_REGISTRY.md`: source hierarchy and data acceptance tests.
- `docs/ERROR_LOG.md`: implementation error history.
- `docs/VALIDATION_LOG.md`: validation history.
- `results/history_extension/`: maximum-history empirical results.
- `results/cost_sensitivity.csv`: fixed cost grid.
- `results/statistical_validation.csv`: bootstrap and sign-test summary.
