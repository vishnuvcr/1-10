# Validation Log

## 2026-09-23

### Static/code review
- Removed current-bar SMA look-ahead.
- Added prior-session SMA target.
- Added explicit causal stop mode.
- Added tests for shifted SMA and position sizing.
- Added workflow trigger for pull-request smoke testing and manual dispatch.

### Environment
- Local Python has numpy 2.3.5, pandas 2.2.3, matplotlib 3.10.8, pytest 9.0.2.
- Local environment lacks yfinance and vectorbt.
- Container DNS cannot resolve github.com.
- No CI workflow run was reported by the GitHub connector for the latest feature commit.

### Status
No historical performance result is certified yet. The next acceptance gate is a CI pass plus a frozen market-data run.
