# Phase 2 Data Freeze and Primary Backtest

## Primary configuration
- Instrument: ^NSEI (Yahoo Finance NIFTY 50 index series).
- Date range: 2010-01-01 through 2026-09-22 inclusive (end=2026-09-23).
- Stop mode: previous_bar_extreme for the primary causal daily run.
- Target: prior-session 21-SMA.
- Monte Carlo: 1,000 paths, seed 42.
- Starting equity: INR 100,000.
- Nominal risk: 1% of current equity.
- Default cost parameters remain explicit in the CLI.

## Why the primary run uses previous-bar stops

The user's literal entry-candle low/high stop is not knowable at the open from daily OHLC. The primary Phase 2 result therefore uses the previous session low/high as the causal comparison. The literal entry-bar mode remains available for sensitivity research.

## Freeze requirements

The workflow writes:
- exact ticker/date configuration;
- raw-data SHA-256;
- first/last data date;
- row count;
- code git SHA;
- strategy/cost parameters;
- Monte Carlo seed/path count.

The exact CSV is retained by the Actions cache and uploaded with the run artifact. It should be promoted to a repository-owned frozen data snapshot only after provenance and schema checks pass.

## Interpretation gate

The Phase 2 run is exploratory until data-schema checks pass, the raw-data hash is recorded, trade count is non-zero and plausibly large enough for inference, transaction-cost sensitivity is run, literal-vs-causal stop sensitivity is compared, and the Monte Carlo distribution is saved and reviewed.

No live-trading claim follows from this phase.
