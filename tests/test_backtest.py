import numpy as np
import pandas as pd

from backtest import (
    CostModel,
    _stop_hit,
    _target_hit,
    add_indicators,
    monte_carlo_simulation,
    position_size,
    run_backtest,
)


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


def flat_data(n=80):
    idx = pd.bdate_range("2024-01-01", periods=n)
    return pd.DataFrame(
        {
            "Open": 100.0,
            "High": 100.0,
            "Low": 100.0,
            "Close": 100.0,
            "Volume": 1000,
        },
        index=idx,
    )


def test_indicator_columns_exist():
    out = add_indicators(synthetic_data())
    assert {"SMA21", "PrevSMA21", "RSI14", "PrevRSI14", "LongSignal", "ShortSignal"} <= set(out.columns)


def test_previous_sma_is_shifted_and_not_current_bar():
    out = add_indicators(synthetic_data())
    expected = out["SMA21"].shift(1)
    valid = expected.notna()
    assert np.allclose(out.loc[valid, "PrevSMA21"], expected.loc[valid])


def test_position_size_risks_one_percent_before_rounding():
    qty, risk = position_size(100000, 100, 90, risk_fraction=0.01, lot_size=1)
    assert qty == 100
    assert risk == 1000


def test_monte_carlo_shape_and_risk_keys():
    results, summary, paths = monte_carlo_simulation(
        [0.01, -0.02, 0.03, -0.01],
        starting_equity=100000,
        n_sims=1000,
        seed=42,
    )
    assert results.shape == (1000, 2)
    assert paths.shape == (1000, 5)
    assert set(summary["risk_of_ruin"]) == {"10%", "20%", "30%", "40%", "50%"}


def test_flat_market_does_not_generate_trades():
    trades, equity, metrics = run_backtest(
        flat_data(),
        costs=CostModel(brokerage_per_order=0, slippage_bps=0),
    )
    assert trades.empty
    assert len(equity) == 80
    assert np.isfinite(metrics["final_equity"])


def test_same_bar_stop_target_conflict_is_stop_first():
    row = pd.Series({"Open": 100.0, "High": 105.0, "Low": 95.0})
    stop_hit, stop_fill = _stop_hit(row, "LONG", 97.0)
    target_hit, target_fill = _target_hit(row, "LONG", 103.0)
    assert stop_hit and target_hit
    assert stop_fill == 97.0
    assert target_fill == 103.0


def test_causal_stop_mode_is_explicit():
    _, _, metrics = run_backtest(
        synthetic_data(),
        costs=CostModel(brokerage_per_order=0, slippage_bps=0),
        stop_mode="previous_bar_extreme",
    )
    assert metrics["NON_CAUSAL_ENTRY_CANDLE_STOP"] is False
    assert metrics["stop_mode"] == "previous_bar_extreme"
