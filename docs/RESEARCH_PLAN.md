# Research Plan - Daily RSI/SMA Gap Reversion

## Research questions
1. Does the locked rule produce positive net-of-costs expectancy on Indian daily data?
2. How sensitive is the result to stop definition, same-day ordering, slippage and brokerage?
3. How variable are final returns and maximum drawdowns under 1,000 bootstrap trade sequences?
4. What is the probability of reaching 10%, 20%, 30%, 40% or 50% peak-to-trough drawdown?
5. Does the observed result persist across instruments and date windows without parameter tuning?

## Locked rules
- 21-period SMA.
- 14-period Wilder RSI.
- Long when yesterday RSI < 10 and today's open < yesterday's close.
- Short when yesterday RSI > 90 and today's open > yesterday's close.
- Entry at today's open.
- Target is the prior-session 21-SMA.
- Literal requested stop: entry-bar extreme; flagged NON-CAUSAL on daily OHLC.
- Causal daily comparison: previous-bar extreme.
- Starting equity INR 100,000.
- Nominal risk 1%.
- One open position at a time.

## Execution policy
- Gap-through fills at the open.
- Same-bar stop/target conflict uses stop-first.
- Integer sizing is rounded down to lot size.
- Costs are explicit parameters.

## Phase gates
### Phase 0 - Governance
COMPLETE.

### Phase 1 - Strategy implementation
COMPLETE. CI passed 7 tests.

### Phase 2 - Data freeze + primary backtest
COMPLETE. NIFTY primary sample froze 4,106 daily rows and produced zero qualifying signals.

### Phase 3 - Cross-sectional + history diagnostic
COMPLETE. Fixed seven-symbol 2010-2026 experiment produced no trades; maximum-history extension produced 15 total completed trades across five trade-bearing symbols.

### Phase 4 - Monte Carlo robustness
COMPLETE WITH INSUFFICIENCY FINDING. 1,000 trade-bootstrap paths were produced where trades existed, but 1-9 observed trades per symbol make the distributions highly sample-limited.

### Phase 5 - Cost sensitivity
COMPLETE. 84 fixed slippage/brokerage combinations.

### Phase 6 - Statistical validation
COMPLETE, DESCRIPTIVE-ONLY. 10,000 bootstrap mean-return resamples and exact sign tests; every symbol remains below n=30.

### Phase 7 - Manuscript
COMPLETE. Full reproducible manuscript, figures, tables, appendices, limitations and future research stored in the repository.

## Stopping rule

Stop after Phase 7. No parameter optimization, regime filter, instrument substitution, or execution-model change is added to this study. Any such change starts a new preregistered research branch.

## Reproducibility contract

Every published result must retain the code SHA, package versions, ticker, date range, raw-data path and SHA-256, parameters, costs, seed, trade ledger, equity curve and statistical outputs.
