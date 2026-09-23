import numpy as np
import pandas as pd

from backtest import CostModel, add_indicators, monte_carlo_simulation, run_backtest


def synthetic_data(n=80):
    idx = pd.bdate_range("2024-01-01", periods=n)
    close = pd.Series(100.0 + np.arange(n) * 0.05, index=idx)
    return pd.DataFrame(
        {
            "Open": close.values,
            "High": close.values + 1,
            "Low": close.values - 1,
            "Close": close.values,
            "Volume": 1000,
        },
        index=idx,
    )


def test_indicator_columns_exist():
    out = add_indicators(synthetic_data())
    assert {"SMA21", "PrevSMA21", "RSI14", "PrevRSI14", "LongSignal", "ShortSignal"} <= set(out.columns)


def test_previous_sma_is_shifted_and_not_current_bar():
    out = add_indicators(synthetic_data())
    valid = out.dropna(subset=["SMA21", "PrevSMA21"])
    assert np.allclose(valid["PrevSMA21"].to_numpy(), valid["SMA21"].shift(1).dropna().to_numpy())


def test_monte_carlo_shape_and_risk_keys():
    results, summary, paths = monte_carlo_simulation([0.01, -0.02, 0.03, -0.01], 100000, 1000, 42)
    assert results.shape == (1000, 2)
    assert paths.shape == (1000, 5)
    assert set(summary["risk_of_ruin"]) == {"10%", "20%", "30%", "40%", "50%"}


def test_empty_trades_do_not_crash_backtest():
    trades, equity, metrics = run_backtest(
        synthetic_data(),
        costs=CostModel(brokerage_per_order=0, slippage_bps=0),
    )
    assert trades.empty
    assert len(equity) == 80
    assert np.isfinite(metrics["final_equity"])
