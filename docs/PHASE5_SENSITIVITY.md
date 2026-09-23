# Phase 5 Cost Sensitivity

## Experiment
Run the locked causal daily strategy on the frozen maximum-history data with no signal/parameter changes.

Cost grid:
- slippage: 0, 5, 10, 20 bps per fill;
- brokerage: INR 0, 20, 40 per executed order;
- exchange/STT/stamp/SEBI rates remain the explicit zero defaults used in the primary run;
- GST remains 18% on modeled brokerage/exchange/SEBI components.

This is a stress test, not optimization. The baseline is 5 bps + INR20/order. The stress case is 20 bps + INR40/order.

## Acceptance
A result is not interpreted as evidence of robustness unless the trade count is sufficient. Given the Phase 3 maximum-history experiment produced at most nine trades for any tested symbol, this cost study is descriptive only.
