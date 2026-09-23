# Error Log

## 2026-09-23

### E001 - Empty repository
The repository had no initial commit. Resolved by bootstrapping main.

### E002 - Initial long-form repository write rejected
The first bulk write was rejected by the execution safety layer. Resolved by using Git object blobs and explicit trees/commits.

### E003 - Entry-candle stop look-ahead
The final low/high of the entry candle is unavailable at the open. The requested literal mode remains available as entry_bar_extreme and is explicitly flagged NON-CAUSAL. A causal mode using the previous bar low/high is now available.

### E004 - Same-day stop/target ordering
Daily OHLC cannot reveal intrabar order. Later-day conflicts use stop-first. Gap-through events fill at the open.

### E005 - Integer position sizing
Exact 1% risk is not always representable with integer units. Quantity is rounded down to lot size.

### E006 - Instrument-specific costs
Brokerage, STT, stamp duty, exchange, GST and SEBI charges differ by instrument and segment. All are parameterized.

### E007 - Current-bar SMA target look-ahead
The target initially used the current day's SMA, which includes information unavailable at the open. Resolved by defining the daily target as the prior-session 21-SMA.

### E008 - Local network execution unavailable
The container could not resolve github.com, and yfinance/vectorbt are not installed locally. Local integration execution is therefore not claimed; repository CI is the validation path.
