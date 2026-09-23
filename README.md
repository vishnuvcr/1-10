# 1-10 Quant Research Repository

## Current research status

Phase 1 of the daily RSI/SMA gap-reversion research suite is under active validation.

- Phase 1 branch: `phase-1-backtest-validation`
- Research plan: `docs/RESEARCH_PLAN.md`
- Phase status: `docs/PHASE_STATUS.md`
- Error log: `docs/ERROR_LOG.md`
- Validation log: `docs/VALIDATION_LOG.md`
- Literature matrix: `docs/LITERATURE_MATRIX.md`
- Data source registry: `docs/DATA_SOURCE_REGISTRY.md`

## Current gate

The dependency conflict found by CI has been resolved. The next CI pass must validate the corrected test fixture and same-day stop/target test. No historical performance result is certified until CI passes and a frozen market-data run is executed.

The strategy implementation explicitly distinguishes the literal user-specified entry-bar stop, which is non-causal on daily OHLC, from a causal previous-bar stop mode. The daily SMA target is based on the prior-session 21-SMA to avoid current-bar look-ahead.
