# Phase 3 Historical Coverage Diagnostic

Purpose: determine whether the zero-signal result is specific to the 2010-2026 sample window.

## Locked rules
- Same 21-SMA and 14-RSI.
- Same RSI thresholds 10/90.
- Same gap conditions.
- Same prior-session SMA target.
- Same previous-bar-extreme causal stop.
- Same INR 100,000 capital, 1% risk, 5 bps slippage, INR 20/order brokerage.
- Same 1,000-trial Monte Carlo and seed 42.

Only the **data start date** is extended to 1990-01-01, using the maximum history available from Yahoo Finance for each symbol. This is a coverage diagnostic, not parameter optimization.

## Decision gate
If all symbols still have zero RSI<10 / RSI>90 observations, the locked strategy has no trade population across both the primary 2010-2026 sample and the maximum-coverage Yahoo sample used here. Monte Carlo remains mathematically undefined because there are no completed trades to resample.
