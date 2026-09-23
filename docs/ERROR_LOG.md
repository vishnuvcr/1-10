# Error Log

## 2026-09-23

E001 - Empty repository. Resolved by bootstrapping main.

E002 - Initial long-form write rejected by the execution safety layer. Resolved with Git object blobs and explicit trees.

E003 - Entry-candle stop look-ahead. Literal entry_bar_extreme remains available but is flagged NON-CAUSAL. previous_bar_extreme is the causal daily comparison.

E004 - Same-day stop/target order is unknowable from daily OHLC. Later-day conflicts use stop-first; gap-through uses the open.

E005 - Integer sizing cannot always represent exactly 1% risk. Quantity is rounded down to lot size.

E006 - Instrument-specific costs differ. Brokerage, STT, stamp, exchange, GST and SEBI charges remain parameterized.

E007 - Current-bar SMA target look-ahead. Resolved by using the prior-session 21-SMA as the daily target.

E008 - Local environment cannot reach github.com and lacks yfinance/vectorbt. Repository CI is the integration-validation path.

E009 - CI dependency conflict. vectorbt 1.1.0 requires pandas >=3.0.3,<4.0 while the previous requirement used pandas <3. Resolved by moving the pandas constraint to >=3.0.3,<4.

E010 - CI test-fixture failure. The original synthetic trending fixture legitimately generated 59 short trades, so the test expecting zero trades was invalid. Resolved with a flat-price fixture and direct stop/target tests.

E011 - Vectorbt reconciliation ambiguity. Daily data cannot represent same-day or multiple-order timestamps with a single price slot. Reconciliation now refuses those cases instead of silently producing a misleading result.

E012 - Phase 2 workflow expression escaping. The first generated YAML preserved backslashes before GitHub expression variables, causing the shell to receive values such as \previous_bar_extreme. Resolved by generating literal GitHub expressions without the extra slash.

E013 - Locked NIFTY 50 signal scarcity. The yfinance sample contains 4,106 daily observations from 2010-01-04 through 2026-09-21. RSI14 min/max are 12.94/85.60, so RSI<10 and RSI>90 never occurred; gap conditions were common (1,428 gap-down and 2,665 gap-up days) but the extreme-RSI gate eliminated every trade.
