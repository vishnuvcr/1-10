# Phase 6 Statistical Validation

## Methods
- 10,000 non-parametric bootstrap resamples of the completed trade-return mean for each symbol.
- 95% percentile interval for the mean trade return.
- Exact two-sided binomial sign test against 50% positive/negative outcomes.
- Pooled trade-return statistics are reported descriptively only and are not treated as independent cross-sectional evidence.
- No Deflated Sharpe Ratio or Probability of Backtest Overfitting estimate is asserted because the research did not perform a parameter-selection tournament; DSR/PBO would be inappropriate as a substitute for that missing multiple-testing structure.

## Interpretation gate
The maximum-history sample produced at most nine trades per symbol. Results with n < 30 are explicitly labeled descriptive-only and are not treated as statistically established edge estimates.
