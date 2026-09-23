# 1-10 - Daily Mean-Reversion Backtest Suite

Phase 1 implementation for the requested daily gap-reversion strategy.

## Rules
- 21-period SMA.
- 14-period Wilder RSI with 10/90 bands.
- Long: yesterday RSI < 10 and today's open < yesterday's close.
- Short: yesterday RSI > 90 and today's open > yesterday's close.
- Entry at today's open.
- Daily target: prior-session 21-SMA.
- Default requested stop mode: entry-bar low/high.
- Causal comparison stop mode: previous-bar low/high.
- INR 100,000 starting equity and 1% nominal risk per trade.
- 1,000 bootstrap Monte Carlo paths.

## Important causality point
The requested entry-bar low/high is not known at the open. The default literal mode is therefore research-only and is flagged NON_CAUSAL_ENTRY_CANDLE_STOP=true. Use --stop-mode previous_bar_extreme for the causal daily comparison, or use intraday data for a true entry-bar stop.

The target uses the previous-session SMA because the current day's closing value is unavailable at the entry open.

## Setup

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    pytest -q

## Local run

    python backtest.py --ticker ^NSEI --start 2010-01-01 --end 2026-09-23 --stop-mode previous_bar_extreme --n-mc 1000 --seed 42 --output-dir results

The ticker is configurable, for example RELIANCE.NS. Use --refresh-data to replace the local Yahoo Finance cache.

## GitHub Actions
The workflow provides both pull-request smoke tests and a manual Run workflow button. The manual inputs include ticker, start/end dates, Monte Carlo path count, seed and cache refresh. The CI environment is the preferred integration-validation path because the local container has no GitHub DNS access.

## Costs
Slippage, fixed brokerage, exchange turnover fees, STT, stamp duty, GST and SEBI turnover fees are explicit parameters. Default brokerage is INR 20 per executed order. Verify the current Paytm Money tariff and statutory charges for the selected instrument/segment before treating net P&L as executable.

## Metrics
Win Rate = fraction of completed trades with positive net P&L.
Sharpe = annualized mean daily equity return divided by daily return standard deviation using 252 periods.
Maximum Drawdown = largest peak-to-trough marked-to-market equity decline.
CAGR and profit factor are also reported.

## Monte Carlo
Completed trade returns are sampled with replacement 1,000 times by default. Each path compounds from INR 100,000. The output reports 5th/25th/50th/75th/95th percentiles for final return and maximum drawdown, plus the probability of reaching 10%, 20%, 30%, 40% or 50% drawdown from a running peak.

## Research files
- docs/RESEARCH_PLAN.md
- docs/PHASE_STATUS.md
- docs/ERROR_LOG.md
- docs/VALIDATION_LOG.md
- docs/CONVERSATION_LOG.md
- tests/test_backtest.py
- .github/workflows/backtest.yml
