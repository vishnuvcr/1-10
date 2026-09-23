# Validation Log

## 2026-09-23

### Static/code review
- Removed current-bar SMA look-ahead.
- Added prior-session SMA target.
- Added explicit causal previous-bar stop mode.
- Added tests for shifted SMA, position sizing, Monte Carlo output shape and causal mode metadata.
- Added pull-request smoke testing and full manual backtest workflow.

### CI finding
GitHub Actions run 35850749739 reached pip install and failed before pytest. The resolver identified a real dependency conflict: vectorbt 1.1.0 requires pandas >=3.0.3,<4.0, while the repository required pandas <3.

### Fix
requirements.txt now requires pandas >=3.0.3,<4. The latest pandas release listed by PyPI is 3.0.6 (17 September 2026). vectorbt 1.1.0 was released 5 July 2026 and yfinance 1.7.0 was released 26 August 2026.

### Status
A new PR validation run is expected after the dependency fix. No historical performance result is certified until CI passes and a frozen market-data run completes.
