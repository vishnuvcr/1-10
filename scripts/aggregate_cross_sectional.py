from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path("results")
rows = []

for path in sorted(ROOT.glob("*/backtest_metrics.json")):
    if path.parent.name == "results":
        continue
    metrics = json.loads(path.read_text(encoding="utf-8"))
    mc_path = path.parent / "monte_carlo_summary.json"
    mc = json.loads(mc_path.read_text(encoding="utf-8")) if mc_path.exists() else {}

    final_p = mc.get("final_return_percentiles", {})
    dd_p = mc.get("max_drawdown_percentiles", {})
    ruin = mc.get("risk_of_ruin", {})

    rows.append(
        {
            "symbol": path.parent.name,
            "trade_count": metrics.get("trade_count", 0),
            "final_equity": metrics.get("final_equity"),
            "final_return": metrics.get("final_return"),
            "cagr": metrics.get("cagr"),
            "max_drawdown": metrics.get("max_drawdown"),
            "sharpe_ratio": metrics.get("sharpe_ratio"),
            "win_rate": metrics.get("win_rate"),
            "profit_factor": metrics.get("profit_factor"),
            "expectancy_per_trade": metrics.get("expectancy_per_trade"),
            "rsi_min": metrics.get("signal_diagnostics", {}).get("rsi_min"),
            "rsi_max": metrics.get("signal_diagnostics", {}).get("rsi_max"),
            "long_signal_count": metrics.get("signal_diagnostics", {}).get("long_signal_count"),
            "short_signal_count": metrics.get("signal_diagnostics", {}).get("short_signal_count"),
            "mc_status": mc.get("status", "executed" if final_p else "not_run"),
            "mc_final_p05": final_p.get("5"),
            "mc_final_p50": final_p.get("50"),
            "mc_final_p95": final_p.get("95"),
            "mc_maxdd_p05": dd_p.get("5"),
            "mc_maxdd_p50": dd_p.get("50"),
            "mc_maxdd_p95": dd_p.get("95"),
            "mc_ruin_10": ruin.get("10%"),
            "mc_ruin_20": ruin.get("20%"),
            "mc_ruin_30": ruin.get("30%"),
            "mc_ruin_40": ruin.get("40%"),
            "mc_ruin_50": ruin.get("50%"),
        }
    )

out = pd.DataFrame(rows)
out.to_csv(ROOT / "cross_sectional_summary.csv", index=False)
(ROOT / "cross_sectional_summary.json").write_text(
    out.to_json(orient="records", indent=2),
    encoding="utf-8",
)
print(out.to_string(index=False))
