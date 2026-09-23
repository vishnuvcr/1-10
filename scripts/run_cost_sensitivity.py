from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backtest import CostModel, run_backtest, validate_ohlcv

SYMBOLS = ["^NSEI", "RELIANCE.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", "TCS.NS", "SBIN.NS"]
SLIPPAGE_BPS = [0.0, 5.0, 10.0, 20.0]
BROKERAGE = [0.0, 20.0, 40.0]

rows = []
for symbol in SYMBOLS:
    cache_path = Path("data/raw") / (symbol.replace("^", "") + ".csv")
    data = validate_ohlcv(pd.read_csv(cache_path, index_col=0, parse_dates=True))

    for slippage in SLIPPAGE_BPS:
        for brokerage in BROKERAGE:
            costs = CostModel(
                slippage_bps=slippage,
                brokerage_per_order=brokerage,
                exchange_txn_rate=0.0,
                stt_buy_rate=0.0,
                stt_sell_rate=0.0,
                stamp_buy_rate=0.0,
                gst_rate=0.18,
                sebi_turnover_rate=0.0,
            )
            trades, equity, metrics = run_backtest(
                data,
                starting_equity=100000.0,
                risk_fraction=0.01,
                lot_size=1,
                costs=costs,
                stop_mode="previous_bar_extreme",
            )
            rows.append(
                {
                    "symbol": symbol,
                    "slippage_bps": slippage,
                    "brokerage_per_order": brokerage,
                    "trade_count": metrics["trade_count"],
                    "final_return": metrics["final_return"],
                    "max_drawdown": metrics["max_drawdown"],
                    "sharpe_ratio": metrics["sharpe_ratio"],
                    "win_rate": metrics["win_rate"],
                    "profit_factor": metrics["profit_factor"],
                    "expectancy_per_trade": metrics["expectancy_per_trade"],
                }
            )

out = pd.DataFrame(rows)
Path("results").mkdir(exist_ok=True)
out.to_csv("results/cost_sensitivity.csv", index=False)
print(out.to_string(index=False))

# Compact per-symbol baseline/stress comparison.
baseline = out[(out["slippage_bps"] == 5.0) & (out["brokerage_per_order"] == 20.0)].copy()
stress = out[(out["slippage_bps"] == 20.0) & (out["brokerage_per_order"] == 40.0)].copy()
comparison = baseline.merge(
    stress,
    on="symbol",
    suffixes=("_baseline", "_stress"),
)
comparison.to_csv("results/cost_sensitivity_baseline_vs_stress.csv", index=False)
