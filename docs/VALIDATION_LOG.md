# Validation Log

## 2026-09-23

- Phase 1 CI: PASS, 7 unit tests.
- Dependency conflict with vectorbt/pandas: detected and fixed.
- Invalid synthetic no-trade fixture: detected and fixed.
- Vectorbt daily same-timestamp reconciliation ambiguity: detected and fail-safe handling added.
- Phase 2 primary NIFTY run: PASS, 4,106 observations, zero qualifying RSI<10/RSI>90 signals.
- Phase 2 data manifest: SHA-256 recorded.
- Phase 3 fixed seven-symbol 2010-2026 run: PASS, zero completed trades.
- Phase 3 maximum-history diagnostic: PASS, 15 completed trades across five symbols.
- Phase 5 fixed cost sensitivity: PASS, 84 combinations.
- Phase 6 statistical validation: first run failed on an empty trade-ledger CSV; validator fixed to treat no-trade ledgers as valid.
- Phase 6 rerun: PASS; 10,000 bootstrap resamples and exact sign tests completed.
- Phase 7 manuscript: COMPLETE.

## Final statistical status

All symbol-level inference is descriptive-only because every symbol has fewer than 30 completed trades.
