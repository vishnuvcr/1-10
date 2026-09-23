# Validation Log

## 2026-09-23

### Static review
- Removed current-bar SMA look-ahead.
- Added prior-session SMA target.
- Added explicit causal previous-bar stop mode.
- Added tests for shifted SMA, position sizing, Monte Carlo output shape, causal mode, flat-market no-signal behavior, and same-day stop/target ordering.

### CI findings
Run 35850749739 failed at dependency installation because vectorbt 1.1.0 requires pandas >=3.0.3,<4. That was fixed.

Run 35851173440 then installed the corrected dependency set successfully, including pandas 3.0.6, vectorbt 1.1.0 and yfinance 1.7.0, but failed one invalid test fixture: the trending fixture generated legitimate short signals. The backtest itself returned 59 trades for that fixture.

### Fix
Replaced the invalid empty-trade fixture with a flat market dataset that has RSI=50 and no gap signals. Added a direct test that both stop and target can be touched on a daily bar and the research policy resolves the ambiguity as stop-first.

### Status
A new validation run must pass all tests before Phase 1 can close.
