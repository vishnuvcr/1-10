# Literature Matrix - Mean Reversion, Technical Rules, and Backtest Robustness

Research status: initial literature gate, 2026-09-23.

| Source | Main contribution | Relevance | Limitation for this strategy |
|---|---|---|---|
| Jegadeesh (1990), *Evidence of Predictable Behavior of Security Returns*, Journal of Finance, DOI 10.1111/j.1540-6261.1990.tb05110.x | Documents negative first-order serial correlation in individual stock returns and related predictability. | Supports testing short-horizon reversal mechanisms rather than assuming all daily returns are iid. | Uses older US data and monthly serial behavior; does not validate this RSI/gap rule or Indian markets. |
| Jegadeesh & Titman (1990), *Short Horizon Reversals and the Bid-Ask Spread* | Links short-horizon negative serial covariance to market-microstructure/inventory mechanisms. | Directly motivates treating transaction costs and execution quality as first-order research variables. | US historical market microstructure; daily OHLC backtests cannot reconstruct intraday bid/ask mechanics. |
| Bailey, Borwein, Lopez de Prado & Zhu (2017), *The Probability of Backtest Overfitting*, Journal of Computational Finance, DOI 10.21314/JCF.2016.322 | Introduces PBO/CSCV for assessing selection risk from repeated backtest experimentation. | Later phases should use explicit multiple-testing / overfitting controls before parameter optimization. | PBO does not make a single pre-specified rule profitable; it is a validation framework. |
| Wijesinghe (2026 preprint), *Do Simple Technical Trading Rules Survive Realistic Costs?* | Tests simple technical rules with walk-forward analysis, realistic costs, bootstrap confidence intervals, DSR and Monte Carlo trade resampling. | Closely aligned with this project's emphasis on costs and trade-level Monte Carlo. | Different markets/data and still a preprint; it is contextual evidence, not validation of the present rule. |
| Pillai (2026 preprint), *Technical-Indicator Strategy Performance in Indian Equities: A Joint Test of Market Efficiency, 2015-2025* | Tests 13 technical-rule configurations on 78 NSE F&O-eligible stocks using Romano-Wolf multiple-testing correction. | Supports explicit multiple-testing control and Indian-market sensitivity analysis. | Preprint; rule family differs from this fixed RSI/gap specification, and reported results cannot be transferred to this exact rule. |

## Research implication

The literature is consistent with testing a short-horizon reversal hypothesis but also with treating microstructure, costs, data-snooping, and regime dependence as material confounders. The project therefore keeps the requested parameters locked and postpones optimization until after the primary result is frozen.

## Primary methodological references

- Jegadeesh (1990), Journal of Finance 45(3), 881-898.
- Jegadeesh & Titman (1990), short-horizon reversal / bid-ask spread literature.
- Bailey et al. (2017), Journal of Computational Finance 20(4), 39-69.
- Future statistical-validation phase: Romano-Wolf family-wise error control, Deflated Sharpe Ratio, CSCV/PBO.
