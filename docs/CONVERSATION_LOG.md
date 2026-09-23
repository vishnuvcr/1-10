# Conversation / Decision Log

## 2026-09-23 - Initial request
Requested a complete Python backtesting suite for the 21-SMA / 14-RSI gap-reversion strategy with 1% equity risk and 1,000-path Monte Carlo robustness analysis.

## 2026-09-23 - Proceed command
Continued automatically without stopping at the first implementation blocker.

## Decisions made
- Primary simulation remains explicit pandas/numpy event-driven because daily OHLC lacks intrabar ordering.
- vectorbt is retained as a reconciliation layer.
- Literal entry-candle stop mode remains available but is explicitly non-causal.
- A causal previous-bar stop mode was added.
- Daily SMA target uses prior-session SMA, not the current closing SMA.
- Costs are explicit parameters.
- Every error and validation limitation is logged in docs/ERROR_LOG.md and docs/VALIDATION_LOG.md.

Private chain-of-thought is not stored; this file records observable decisions and validation events only.
