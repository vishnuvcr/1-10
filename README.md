# 1-10 Quant Research Repository

## Current research status

The repository has an active Phase 1 branch implementing the daily RSI/SMA gap-reversion backtest and Monte Carlo robustness suite.

- Phase 1 branch: phase-1-backtest-foundation
- Research plan: docs/RESEARCH_PLAN.md
- Phase status: docs/PHASE_STATUS.md
- Error log: docs/ERROR_LOG.md
- Validation log: docs/VALIDATION_LOG.md

The project is intentionally separating the literal user-specified entry-bar stop from a causal daily comparison so that look-ahead is not hidden inside reported results.
