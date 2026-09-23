# Conversation / Decision Log

## 2026-09-23 — User request
Requested a complete Python suite for a daily mean-reversion strategy using 21-SMA, 14-RSI with 10/90 extremes, gap-down long and gap-up short entries, entry at the open, entry-candle low/high stop, SMA take-profit, INR 100,000 initial capital, 1% equity risk, and a 1,000-path trade-return Monte Carlo analysis with drawdown risk-of-ruin.

Requested files: requirements.txt, backtest.py, README.md, plus local/Codespaces instructions and explicit edge-case handling.

## Observable implementation decisions
- Explicit pandas/numpy event-driven simulation is the primary ledger.
- vectorbt is used as a reconciliation layer.
- Local data cache is preferred to repeated downloads.
- The literal entry-candle stop is flagged as non-causal with daily bars.
- Later-day stop/target ambiguity uses a conservative stop-first rule.
- All cost assumptions are explicit parameters.

Private chain-of-thought is not stored; this log records user requirements and observable decisions only.
