# 1-10 Quant Research — Daily Mean-Reversion Backtest Suite

Phase 1 implementation for the requested daily gap-reversion strategy.

## Strategy
- 21-period SMA.
- 14-period RSI.
- Long when yesterday RSI is below 10 and today's open is below yesterday's close.
- Short when yesterday RSI is above 90 and today's open is above yesterday's close.
- Entry at today's open.
- Stop reference uses the entry candle low for longs and high for shorts.
- Exit at the first SMA touch/cross.
- Starting equity INR 100,000; nominal risk 1% of current equity.

## Critical daily-bar limitation
The final low/high of an entry candle is not known at that candle's open. The literal requested sizing rule is therefore non-causal with daily OHLC. The code flags NON_CAUSAL_ENTRY_CANDLE_STOP=true and activates that stop from the next session. A causal research phase must use an ex-ante stop or intraday data. When stop and SMA target are both touched on a later daily bar, the code assumes stop-first because intrabar order is unknowable.

## Setup

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    pytest -q

## Run

    python backtest.py --ticker ^NSEI --start 2010-01-01 --end 2026-09-23 --n-mc 1000 --seed 42 --output-dir results

Use --refresh-data to replace the local CSV cache under data/raw. The ticker is configurable, for example RELIANCE.NS.

## Codespaces and GitHub Actions
Codespaces uses the same setup and command sequence above. The manual workflow at .github/workflows/backtest.yml provides a Run workflow button for a smoke-test pass. The next Phase 1 revision should add workflow inputs for ticker, dates, Monte Carlo count and cache refresh.

## Costs
The backtester models slippage, fixed brokerage, exchange turnover fees, STT, stamp duty, GST and SEBI turnover fees as parameters. Default brokerage is INR 20 per executed order. Confirm current Paytm Money and statutory charges for the selected instrument before using net P&L as an executable estimate.

## Standard metrics
Win Rate is the fraction of completed trades with positive net P&L. Sharpe Ratio is annualized daily-return mean divided by daily-return standard deviation using 252 periods. Maximum Drawdown is the largest peak-to-trough marked-to-market equity decline. Also inspect trade count, expectancy and profit factor.

## Monte Carlo
The Monte Carlo module resamples completed trade returns with replacement 1,000 times by default. Each path compounds from INR 100,000. It reports 5th, 25th, 50th, 75th and 95th percentiles for final return and maximum drawdown, plus the probability of reaching 10%, 20%, 30%, 40% and 50% drawdown from a running peak. These paths represent order variability in the observed trade distribution, not new market data.

## Research files
See docs/RESEARCH_PLAN.md, docs/PHASE_STATUS.md, docs/ERROR_LOG.md and docs/CONVERSATION_LOG.md.
