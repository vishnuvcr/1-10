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

E009 - CI dependency conflict. vectorbt 1.1.0 requires pandas >=3.0.3 and <4.0, while requirements previously pinned pandas <3. Resolved by moving the pandas constraint to >=3.0.3,<4.
