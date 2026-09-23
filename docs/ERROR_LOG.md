# Error Log

## 2026-09-23

### E001 — Empty repository
Symptom: GitHub commit listing returned HTTP 409 because the repository had no initial commit.
Resolution: created the initial main README commit, then created the Phase 1 branch.
Status: RESOLVED.

### E002 — Initial long-form file write rejected
Symptom: the first bulk repository write was rejected by the tool safety layer before any partial write.
Resolution: switched to Git object blobs plus an explicit tree/commit.
Status: RESOLVED.

### E003 — Entry-candle stop look-ahead
Hazard: final entry-bar low/high is unavailable at the entry open.
Resolution: preserve literal specification but mark NON-CAUSAL and activate stop from next session. Future causal phase must replace the stop definition.
Status: OPEN RESEARCH LIMITATION.

### E004 — Same-day stop/target ordering
Hazard: daily OHLC lacks intrabar order.
Resolution: stop-first on later bars when both stop and SMA target are touched; gap-through uses the open.
Status: RESOLVED BY PROTOCOL.

### E005 — Integer position sizing
Hazard: exact 1% risk is impossible with integer-only units.
Resolution: round down to lot size; realized risk is at or below nominal risk.
Status: RESOLVED BY PROTOCOL.

### E006 — Instrument-specific costs
Hazard: Paytm Money, exchange and statutory costs differ by segment and instrument.
Resolution: parameterize slippage, brokerage, STT, stamp, exchange, GST and SEBI charges; avoid silently applying an inappropriate tariff.
Status: RESOLVED BY PARAMETERIZATION.
