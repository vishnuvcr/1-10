# Research Plan — Daily RSI/SMA Gap Reversion

## Research questions
1. Does the pre-specified rule produce positive net-of-costs expectancy on daily Indian-market data?
2. How sensitive are results to the entry-candle stop interpretation, same-day ordering, slippage, and brokerage?
3. How stable are final returns and maximum drawdowns under 1,000 trade-sequence bootstrap paths?
4. What is the probability of reaching 10%, 20%, 30%, 40%, and 50% peak-to-trough drawdown?
5. Do results persist across symbols and date windows without parameter tuning?

## Locked strategy
- SMA: 21 periods.
- RSI: 14 periods, Wilder-style smoothing.
- Long: yesterday RSI < 10 and today's open < yesterday's close.
- Short: yesterday RSI > 90 and today's open > yesterday's close.
- Entry at today's open.
- Stop reference: low/high of entry candle.
- Take profit: first SMA touch/cross.
- Starting equity: INR 100,000.
- Nominal risk: 1% current equity per trade.
- One open position at a time.

## Critical interpretation
Daily OHLC does not reveal the final low/high of today's entry candle at the moment the open is traded. Therefore the literal stop/sizing rule is non-causal. The implementation preserves it for reproducibility, flags NON_CAUSAL_ENTRY_CANDLE_STOP=true, and activates the stop from the following session. A future causal phase must use an ex-ante stop or intraday data.

When a later daily bar touches both stop and SMA target, intrabar order is unknowable, so the conservative policy is stop first. Gap-through events fill at the open. Integer sizing is rounded down to lot size.

## Phases
### Phase 0 — Governance / bootstrap
COMPLETE. Repository branch model, plan, status, error log, and decision log established.

### Phase 1 — Strategy implementation
IN PROGRESS. Data cache, indicators, explicit fills, risk sizing, costs, Monte Carlo, vectorbt reconciliation, tests, and manual workflow.

Exit gate: tests pass, edge cases are deterministic, and one run is reproducible from frozen data plus seed.

### Phase 2 — Data acquisition and freeze
NOT STARTED. Freeze the exact raw CSV, validate missing/duplicate bars, corporate actions, timezone, and source metadata.

### Phase 3 — Primary backtest
NOT STARTED. Report trade count, win rate, expectancy, profit factor, Sharpe, max drawdown, CAGR, and complete trade ledger.

### Phase 4 — Monte Carlo robustness
IMPLEMENTED, NOT EXECUTED. Bootstrap completed trade returns with replacement, 1,000 paths, final-return percentiles, max-drawdown percentiles, and drawdown risk-of-ruin.

### Phase 5 — Sensitivity
NOT STARTED. Slippage/brokerage grids, alternate date windows, alternate liquid instruments, and causal-vs-literal execution comparison.

### Phase 6 — Statistical validation
NOT STARTED. Bootstrap confidence intervals, benchmark comparison, and later DSR/PBO analysis after the primary result is frozen.

### Phase 7 — Manuscript
NOT STARTED. Methods, data provenance, results, tables, plots, limitations, conclusion, future research.

## Reproducibility contract
Record git SHA, Python/package versions, ticker, date range, raw-data hash/path, strategy parameters, costs, Monte Carlo seed/path count, execution mode, and known errors for every published result.
