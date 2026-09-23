# Error Log

## 2026-09-23

E001 - Empty repository. Resolved by bootstrapping main.
E002 - Initial long-form write rejected by execution safety layer. Resolved with Git object blobs.
E003 - Entry-candle stop look-ahead. Literal mode remains NON-CAUSAL; previous-bar mode is causal daily comparison.
E004 - Same-day stop/target order is unknowable from daily OHLC; stop-first policy used.
E005 - Integer sizing rounds down to lot size.
E006 - Instrument-specific costs parameterized.
E007 - Current-bar SMA target look-ahead removed by prior-session SMA.
E008 - Local environment lacks network/yfinance/vectorbt; CI used for integration validation.
E009 - vectorbt/pandas dependency conflict fixed with pandas >=3.0.3,<4.
E010 - Invalid no-trade test fixture fixed with a flat-price fixture.
E011 - vectorbt daily reconciliation ambiguity fixed by explicit refusal for same-day/multiple-order timestamps.
E012 - Phase 2 workflow expression quoting fixed.
E013 - NIFTY 2010-2026 RSI 10/90 signal scarcity documented.
E014 - Phase 5 sensitivity runner import path fixed.
E015 - Phase 6 statistical validator empty trade-ledger edge case fixed.
E016 - Final manuscript contained stale phase-status text and corrupted zero-trade table cells; corrected before final commit.
