# Research Plan - Daily RSI/SMA Gap Reversion

## Questions
1. Does the locked rule produce positive net-of-costs expectancy on Indian daily data?
2. How sensitive is the result to stop definition, same-day ordering, slippage and brokerage?
3. How variable are final returns and maximum drawdowns under 1,000 bootstrap trade sequences?
4. What is the probability of reaching 10%, 20%, 30%, 40% or 50% peak-to-trough drawdown?
5. Does any observed result persist across instruments and date windows without parameter tuning?

## Locked rules
- 21-period SMA.
- 14-period Wilder RSI.
- Long when yesterday RSI < 10 and today's open < yesterday's close.
- Short when yesterday RSI > 90 and today's open > yesterday's close.
- Entry at today's open.
- Target is the prior-session 21-SMA for a causal daily implementation.
- Default requested stop mode entry_bar_extreme: today's entry-bar low/high. This is non-causal for sizing.
- Causal comparison stop mode previous_bar_extreme: previous session low/high.
- Starting equity INR 100,000.
- Nominal risk 1% of current equity.
- One open position at a time.

## Execution policy
- Open gaps through a stop/target fill at the open.
- If both stop and target are touched on a later daily bar, stop is assumed first.
- Literal entry-bar stop mode does not activate that stop until the next session.
- Causal previous-bar stop mode is active on the entry session.
- Integer quantity is floored to the lot size.
- All modeled trading costs are explicit parameters.

## Phases
### Phase 0 - Governance
COMPLETE.

### Phase 1 - Strategy implementation
IN PROGRESS at 85%. Code, tests, cost model, Monte Carlo, cache, reconciliation and workflow are implemented.

### Phase 2 - Data acquisition and freeze
NOT STARTED. Freeze exact raw CSV, validate missing/duplicate bars, corporate actions, timezone and source metadata.

### Phase 3 - Primary backtest
NOT STARTED. Run both literal and causal stop modes where data permits, without parameter optimization.

### Phase 4 - Monte Carlo
IMPLEMENTED, NOT EXECUTED. 1,000 with-replacement trade-return paths, final-return and max-drawdown percentiles, drawdown risk-of-ruin.

### Phase 5 - Sensitivity
NOT STARTED. Slippage, brokerage, date-window, instrument and stop-mode sensitivities.

### Phase 6 - Statistical validation
NOT STARTED. Bootstrap intervals, benchmark comparison, and later DSR/PBO after the primary result is frozen.

### Phase 7 - Manuscript
NOT STARTED. Full methods, data provenance, results, figures, limitations, conclusion and future work.

## Reproducibility
Record git SHA, package versions, ticker, date range, raw-data hash/path, strategy parameters, costs, Monte Carlo seed and path count, and execution mode for every published result.
