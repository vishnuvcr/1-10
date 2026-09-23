from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import binomtest

SYMBOLS = ["^NSEI", "RELIANCE.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", "TCS.NS", "SBIN.NS"]
B = 10000
SEED = 42

rng = np.random.default_rng(SEED)
rows = []

for symbol in SYMBOLS:
    path = Path("results/history_extension") / symbol.replace("^", "") / "trades.csv"
    if not path.exists():
        rows.append({"symbol": symbol, "trade_count": 0, "status": "missing_trades_file"})
        continue

    try:
        trades = pd.read_csv(path)
    except pd.errors.EmptyDataError:
        trades = pd.DataFrame()

    if trades.empty:
        rows.append({
            "symbol": symbol,
            "trade_count": 0,
            "status": "no_trades",
        })
        continue

    returns = trades["return_on_equity"].to_numpy(dtype=float)
    returns = returns[np.isfinite(returns)]
    n = len(returns)

    # Non-parametric bootstrap CI for the mean trade return.
    sampled = rng.choice(returns, size=(B, n), replace=True)
    means = sampled.mean(axis=1)
    ci_low, ci_high = np.percentile(means, [2.5, 97.5])

    wins = int((returns > 0).sum())
    sign = binomtest(wins, n=n, p=0.5, alternative="two-sided")

    rows.append(
        {
            "symbol": symbol,
            "trade_count": n,
            "mean_trade_return": float(returns.mean()),
            "median_trade_return": float(np.median(returns)),
            "bootstrap_mean_ci_low": float(ci_low),
            "bootstrap_mean_ci_high": float(ci_high),
            "bootstrap_prob_mean_positive": float((means > 0).mean()),
            "wins": wins,
            "losses": int(n - wins),
            "sign_test_pvalue": float(sign.pvalue),
            "inference_status": (
                "descriptive_only_n<30"
                if n < 30
                else "candidate_for_inference"
            ),
        }
    )

out = pd.DataFrame(rows)
Path("results").mkdir(exist_ok=True)
out.to_csv("results/statistical_validation.csv", index=False)
Path("results/statistical_validation.json").write_text(
    out.to_json(orient="records", indent=2),
    encoding="utf-8",
)

# Pooled descriptive view only; symbol-level independence is not assumed.
pooled = []
all_returns = []
for row in rows:
    if row.get("trade_count", 0) and row.get("status") is None:
        all_returns.extend(
            pd.read_csv(
                Path("results/history_extension") / row["symbol"].replace("^", "") / "trades.csv"
            )["return_on_equity"].dropna().tolist()
        )
if all_returns:
    x = np.asarray(all_returns, dtype=float)
    pooled.append(
        {
            "pooled_trade_count": len(x),
            "pooled_mean_trade_return": float(x.mean()),
            "pooled_median_trade_return": float(np.median(x)),
        }
    )
Path("results/statistical_validation_pooled.json").write_text(
    json.dumps(pooled, indent=2),
    encoding="utf-8",
)

print(out.to_string(index=False))
print(json.dumps(pooled, indent=2))
