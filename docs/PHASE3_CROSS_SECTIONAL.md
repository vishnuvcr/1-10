# Phase 3 Cross-Sectional Robustness

## Fixed experiment

No strategy parameter is optimized in this phase. The same locked rule is run on:

- NIFTY 50 index control: ^NSEI
- RELIANCE.NS
- HDFCBANK.NS
- ICICIBANK.NS
- INFY.NS
- TCS.NS
- SBIN.NS

Primary mode:
- previous-bar extreme stop (causal daily comparison)
- prior-session 21-SMA target
- 1% nominal equity risk
- INR 100,000 starting equity
- 5 bps slippage
- INR 20 brokerage per executed order
- 1,000 trade-bootstrap Monte Carlo paths
- seed 42

## Why this phase exists

The Phase 2 NIFTY 50 control produced no qualifying RSI<10 or RSI>90 observations from the selected 2010-2026 daily sample. This does not mean the general rule is profitable or unprofitable; it means the exact rule has no trade population on that instrument/sample.

Cross-sectional execution tests whether the same locked rule produces a measurable trade population in liquid Indian equities without changing the thresholds.

## Interpretation guardrails

- Each symbol is a separate backtest with its own equity curve.
- Results are not pooled before inspecting trade counts and cost sensitivity.
- A small trade count is treated as insufficient evidence even if return is large.
- Stock short-side economics are not equivalent to index/futures execution; this is a research comparison, not a broker execution claim.
