# Data Source Registry

## Source hierarchy

### Tier 1 - Exchange / regulator
1. NSE official historical reports and equity/derivatives bhavcopy archives.
2. NSE official paid EOD/historical order-and-trade data when tick/order precision is required.
3. NSE historical index data.
4. RBI reference/risk-free series where required.
5. SEBI primary publications for market-structure and participant-cost context.

NSE's current reporting architecture exposes equity bhavcopy/common bhavcopy, security-wise price/volume data, historical index data, F&O contract-wise price/volume data, daily settlement/OI and participant statistics. NSE also states that formal historical-data dissemination includes bhavcopy, index, masters, snapshots, trades and circulars.

### Tier 2 - Reproducibility / open research
- yfinance: convenient reproducible acquisition for the prototype, but not an exchange-certified historical record.
- GitHub NIFTY/Indian-market datasets: cross-checks only until schema, provenance, completeness and corporate-action handling are independently validated.
- Kaggle datasets: useful for coverage discovery and cross-checks, never treated as primary evidence without source reconciliation.

## Sources identified for cross-checking

- qubiit/NIFTY-50-Stock-Market-Data - daily NIFTY-50 stock OHLC from 2016 onward, sourced from NSE bhavcopy/UDiFF and monthly updates.
- Kaldhen-Lepcha/Historical-Data - daily OHLCV for NIFTY constituents, 2020-2025 coverage.
- Thwenat123/nifty50-stock-data-INDIA - broad daily OHLCV history for Indian/NIFTY constituents.
- Hareeshkesavan/Stock-Market-Dataset - annual NIFTY 50 data plus India VIX/FII/DII-related datasets.
- Public Kaggle NIFTY 50 datasets spanning long historical periods, used only as secondary cross-checks.

## Acceptance tests for a frozen dataset

1. Unique trading dates and no duplicate symbol-date rows.
2. OHLC sanity: High >= max(Open, Close), Low <= min(Open, Close), all positive.
3. Calendar validation against an NSE trading calendar.
4. Corporate-action reconciliation where individual equities are used.
5. Explicit treatment of adjusted vs unadjusted prices.
6. No forward-filled OHLC values.
7. Documented timezone and date convention.
8. Dataset start/end coverage recorded exactly.
9. SHA-256 hash of every frozen raw file.
10. Re-run without network access must reproduce the same backtest inputs.

## Execution-data escalation

Daily OHLC is insufficient for reconstructing intraday stop/target ordering. If the entry-candle stop is retained literally, the research should escalate to intraday data and reconstruct the within-bar path rather than inferring it from daily OHLC.
