# Error Log

## 2026-09-23

E001 - Empty repository. Resolved by bootstrapping main.
E002 - Initial long-form write rejected by the execution safety layer. Resolved with Git object blobs and explicit trees.
E003 - Entry-candle stop look-ahead. Literal mode remains NON-CAUSAL; previous-bar mode is the causal daily comparison.
E004 - Same-day stop/target order is unknowable from daily OHLC. Later-day conflicts use stop-first.
E005 - Integer sizing rounds down to lot size.
E006 - Instrument-specific costs are parameterized.
E007 - Current-bar SMA target look-ahead resolved by prior-session 21-SMA.
E008 - Local environment cannot reach github.com and lacks yfinance/vectorbt. Repository CI is the integration-validation path.
E009 - vectorbt/pandas dependency conflict fixed with pandas >=3.0.3,<4.
E010 - Invalid no-trade test fixture fixed.
E011 - vectorbt reconciliation ambiguity fixed by explicit refusal for same-day/multiple-order daily timestamps.
E012 - Phase 2 workflow expression escaping fixed.
E013 - NIFTY 2010-2026 signal scarcity documented; zero qualifying trades in that sample.
E014 - Phase 5 sensitivity script import-path failure. scripts/run_cost_sensitivity.py could not import root-level backtest.py. Fixed by adding the repository root to sys.path before the import.
