# Phase 1 Research Findings

Status: implementation gate, no historical performance finding certified.

## Confirmed implementation findings

1. The original literal entry-candle low/high stop is non-causal with daily OHLC because the completed entry candle is not known at the entry open.
2. The daily SMA target must be based on information known before the entry bar closes. The implementation therefore uses the prior-session 21-SMA for causal daily execution.
3. Later-day stop/target conflicts remain ambiguous in daily OHLC. The explicit conservative policy is stop-first.
4. Transaction costs are configurable and are not silently assumed to be zero.
5. Monte Carlo resampling is defined on completed trade returns, with replacement, preserving the empirical trade-return distribution while destroying historical trade order.
6. No market-performance conclusion should be inferred until a frozen data run passes the acceptance gate.

## Current empirical status

- Historical data acquisition: NOT CERTIFIED.
- Primary backtest: NOT EXECUTED.
- Monte Carlo robustness: CODE IMPLEMENTED, NOT EXECUTED.
- CI integration: dependency conflict was found and fixed; the new default-branch validation runner has been created and is being used to validate the Phase 1 branch.
- Causal execution mode: IMPLEMENTED.
