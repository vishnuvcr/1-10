
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf


@dataclass(frozen=True)
class CostModel:
    slippage_bps: float = 5.0
    brokerage_per_order: float = 20.0
    exchange_txn_rate: float = 0.0
    stt_buy_rate: float = 0.0
    stt_sell_rate: float = 0.0
    stamp_buy_rate: float = 0.0
    gst_rate: float = 0.18
    sebi_turnover_rate: float = 0.0


@dataclass
class Position:
    side: str
    entry_date: pd.Timestamp
    entry_price: float
    entry_fill: float
    stop: float
    qty: int
    entry_equity: float
    entry_cost: float


@dataclass
class Trade:
    side: str
    entry_date: str
    exit_date: str
    qty: int
    entry_price: float
    entry_fill: float
    stop: float
    exit_fill: float
    reason: str
    target_sma: float
    entry_equity: float
    pnl: float
    return_on_equity: float
    entry_cost: float
    exit_cost: float


def safe_name(ticker: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", ticker).strip("_") or "ticker"


def current_git_sha() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL, text=True
        ).strip()
    except Exception:
        return None


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    if isinstance(df.columns, pd.MultiIndex):
        first_level = list(dict.fromkeys(df.columns.get_level_values(0)))
        price_fields = {"Open", "High", "Low", "Close", "Adj Close", "Volume"}
        if set(first_level).intersection(price_fields):
            df.columns = df.columns.get_level_values(0)
        else:
            df.columns = df.columns.get_level_values(1)

    required = ["Open", "High", "Low", "Close"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required OHLC columns: {missing}")

    keep = [c for c in ["Open", "High", "Low", "Close", "Adj Close", "Volume"] if c in df.columns]
    out = df[keep].copy()
    out.index = pd.to_datetime(out.index)
    if getattr(out.index, "tz", None) is not None:
        out.index = out.index.tz_convert(None)
    out = out[~out.index.duplicated(keep="last")].sort_index()
    out = out.dropna(subset=required)

    if (out["High"] < out["Low"]).any():
        raise ValueError("Found High < Low in downloaded data.")
    if (out[["Open", "High", "Low", "Close"]] <= 0).any().any():
        raise ValueError("Found non-positive OHLC value.")
    return out


def fetch_daily_data(
    ticker: str,
    start: str,
    end: str | None = None,
    cache_dir: str | Path = "data/raw",
    refresh: bool = False,
) -> pd.DataFrame:
    cache = Path(cache_dir)
    cache.mkdir(parents=True, exist_ok=True)
    cache_path = cache / f"{safe_name(ticker)}.csv"
    start_ts = pd.Timestamp(start)
    end_ts = pd.Timestamp(end) if end else None

    if cache_path.exists() and not refresh:
        cached = validate_ohlcv(pd.read_csv(cache_path, index_col=0, parse_dates=True))
        covers_start = cached.index.min() <= start_ts
        covers_end = end_ts is None or cached.index.max() >= end_ts - pd.Timedelta(days=7)
        if covers_start and covers_end:
            out = cached.loc[cached.index >= start_ts]
            if end_ts is not None:
                out = out.loc[out.index < end_ts]
            if len(out) >= 30:
                return out

    raw = yf.download(
        ticker,
        start=start,
        end=end,
        auto_adjust=False,
        progress=False,
        actions=False,
        threads=False,
    )
    data = validate_ohlcv(raw)
    data.to_csv(cache_path)
    return data


def compute_rsi_wilder(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0.0)
    loss = -delta.clip(upper=0.0)
    avg_gain = gain.ewm(alpha=1 / period, adjust=False, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1 / period, adjust=False, min_periods=period).mean()
    rs = avg_gain / avg_loss.replace(0.0, np.nan)
    rsi = 100.0 - (100.0 / (1.0 + rs))
    rsi = rsi.where(avg_loss != 0.0, 100.0)
    rsi = rsi.where(~((avg_gain == 0.0) & (avg_loss == 0.0)), 50.0)
    return rsi


def add_indicators(
    df: pd.DataFrame,
    sma_period: int = 21,
    rsi_period: int = 14,
) -> pd.DataFrame:
    out = df.copy()
    out["SMA21"] = out["Close"].rolling(sma_period, min_periods=sma_period).mean()
    out["PrevSMA21"] = out["SMA21"].shift(1)
    out["RSI14"] = compute_rsi_wilder(out["Close"], rsi_period)
    out["PrevRSI14"] = out["RSI14"].shift(1)
    out["PrevClose"] = out["Close"].shift(1)
    out["LongSignal"] = (out["PrevRSI14"] < 10.0) & (out["Open"] < out["PrevClose"])
    out["ShortSignal"] = (out["PrevRSI14"] > 90.0) & (out["Open"] > out["PrevClose"])
    return out


def position_size(
    equity: float,
    entry_price: float,
    stop_price: float,
    risk_fraction: float = 0.01,
    lot_size: int = 1,
) -> tuple[int, float]:
    distance = abs(entry_price - stop_price)
    if not np.isfinite(distance) or distance <= 0:
        return 0, 0.0
    risk_cash = equity * risk_fraction
    raw_qty = risk_cash / distance
    qty = int(math.floor(raw_qty / lot_size) * lot_size)
    return qty, risk_cash


def _executed_side(side: str, is_entry: bool) -> str:
    if side == "LONG":
        return "BUY" if is_entry else "SELL"
    return "SELL" if is_entry else "BUY"


def transaction_cost(
    price: float,
    quantity: int,
    side: str,
    is_entry: bool,
    model: CostModel,
) -> float:
    turnover = float(price) * int(quantity)
    executed_side = _executed_side(side, is_entry)
    brokerage = model.brokerage_per_order
    exchange = turnover * model.exchange_txn_rate
    stt = turnover * (
        model.stt_buy_rate if executed_side == "BUY" else model.stt_sell_rate
    )
    stamp = turnover * model.stamp_buy_rate if executed_side == "BUY" else 0.0
    sebi = turnover * model.sebi_turnover_rate
    gst = model.gst_rate * (brokerage + exchange + sebi)
    return brokerage + exchange + stt + stamp + sebi + gst


def adverse_fill(price: float, side: str, is_entry: bool, slippage_bps: float) -> float:
    slip = slippage_bps / 10000.0
    executed_side = _executed_side(side, is_entry)
    if executed_side == "BUY":
        return price * (1.0 + slip)
    return price * (1.0 - slip)


def _target_hit(row: pd.Series, side: str, target: float) -> tuple[bool, float]:
    if not np.isfinite(target):
        return False, np.nan
    if side == "LONG":
        if row["Open"] >= target:
            return True, float(row["Open"])
        if row["High"] >= target:
            return True, float(target)
    else:
        if row["Open"] <= target:
            return True, float(row["Open"])
        if row["Low"] <= target:
            return True, float(target)
    return False, np.nan


def _stop_hit(row: pd.Series, side: str, stop: float) -> tuple[bool, float]:
    if side == "LONG":
        if row["Open"] <= stop:
            return True, float(row["Open"])
        if row["Low"] <= stop:
            return True, float(stop)
    else:
        if row["Open"] >= stop:
            return True, float(row["Open"])
        if row["High"] >= stop:
            return True, float(stop)
    return False, np.nan


def _close_trade(
    position: Position,
    exit_price_raw: float,
    exit_date: pd.Timestamp,
    exit_reason: str,
    target_sma: float,
    cash: float,
    model: CostModel,
) -> tuple[Trade, float]:
    exit_fill = adverse_fill(
        exit_price_raw,
        position.side,
        is_entry=False,
        slippage_bps=model.slippage_bps,
    )
    exit_cost = transaction_cost(
        exit_fill, position.qty, position.side, is_entry=False, model=model
    )

    if position.side == "LONG":
        cash += exit_fill * position.qty - exit_cost
        gross_pnl = (exit_fill - position.entry_fill) * position.qty
    else:
        cash -= exit_fill * position.qty + exit_cost
        gross_pnl = (position.entry_fill - exit_fill) * position.qty

    pnl = gross_pnl - position.entry_cost
    trade_return = pnl / position.entry_equity if position.entry_equity else np.nan

    trade = Trade(
        side=position.side,
        entry_date=str(position.entry_date.date()),
        exit_date=str(exit_date.date()),
        qty=position.qty,
        entry_price=position.entry_price,
        entry_fill=position.entry_fill,
        stop=position.stop,
        exit_fill=exit_fill,
        reason=exit_reason,
        target_sma=float(target_sma) if np.isfinite(target_sma) else np.nan,
        entry_equity=position.entry_equity,
        pnl=float(pnl),
        return_on_equity=float(trade_return),
        entry_cost=float(position.entry_cost),
        exit_cost=float(exit_cost),
    )
    return trade, cash


def calculate_metrics(
    trades: pd.DataFrame,
    equity: pd.DataFrame,
    starting_equity: float,
) -> dict:
    final_equity = float(equity["Equity"].iloc[-1]) if len(equity) else starting_equity
    final_return = final_equity / starting_equity - 1.0

    if len(equity):
        running_max = equity["Equity"].cummax()
        drawdown = equity["Equity"] / running_max - 1.0
        max_drawdown = float(drawdown.min())
        daily_returns = equity["Equity"].pct_change().replace(
            [np.inf, -np.inf], np.nan
        ).fillna(0.0)
        daily_std = daily_returns.std(ddof=1)
        sharpe = (
            math.sqrt(252.0) * daily_returns.mean() / daily_std
            if daily_std > 0
            else 0.0
        )
        years = max(
            (equity.index[-1] - equity.index[0]).days / 365.25,
            1 / 365.25,
        )
        cagr = (final_equity / starting_equity) ** (1.0 / years) - 1.0
    else:
        max_drawdown = 0.0
        sharpe = 0.0
        cagr = 0.0

    if len(trades):
        wins = trades.loc[trades["pnl"] > 0, "pnl"]
        losses = trades.loc[trades["pnl"] < 0, "pnl"]
        gross_profit = float(wins.sum())
        gross_loss = float(-losses.sum())
        win_rate = float((trades["pnl"] > 0).mean())
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else math.inf
        expectancy = float(trades["pnl"].mean())
    else:
        gross_profit = 0.0
        gross_loss = 0.0
        win_rate = 0.0
        profit_factor = 0.0
        expectancy = 0.0

    return {
        "starting_equity": float(starting_equity),
        "final_equity": final_equity,
        "final_return": float(final_return),
        "cagr": float(cagr),
        "max_drawdown": max_drawdown,
        "sharpe_ratio": float(sharpe),
        "trade_count": int(len(trades)),
        "win_rate": win_rate,
        "profit_factor": float(profit_factor),
        "expectancy_per_trade": expectancy,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
    }


def run_backtest(
    df: pd.DataFrame,
    starting_equity: float = 100000.0,
    risk_fraction: float = 0.01,
    lot_size: int = 1,
    costs: CostModel | None = None,
    stop_mode: str = "entry_bar_extreme",
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    if stop_mode not in {"entry_bar_extreme", "previous_bar_extreme"}:
        raise ValueError("stop_mode must be entry_bar_extreme or previous_bar_extreme")

    model = costs or CostModel()
    data = add_indicators(df)
    cash = float(starting_equity)
    position: Position | None = None
    trades: list[Trade] = []
    equity_rows: list[dict] = []
    dates = list(data.index)

    for i, dt in enumerate(dates):
        row = data.loc[dt]

        # A daily bar cannot reveal the intrabar order between stop and target.
        # We therefore assume STOP first whenever both are touched on the same bar.
        if position is not None and i > 0:
            target = float(row["PrevSMA21"]) if np.isfinite(row["PrevSMA21"]) else np.nan
            stop_hit, stop_fill = _stop_hit(row, position.side, position.stop)
            target_hit, target_fill = _target_hit(row, position.side, target)

            if stop_hit and target_hit:
                trade, cash = _close_trade(
                    position, stop_fill, dt, "STOP_SAME_BAR_CONSERVATIVE",
                    target, cash, model
                )
                trades.append(trade)
                position = None
            elif stop_hit:
                trade, cash = _close_trade(
                    position, stop_fill, dt, "STOP", target, cash, model
                )
                trades.append(trade)
                position = None
            elif target_hit:
                trade, cash = _close_trade(
                    position, target_fill, dt, "SMA_TARGET", target, cash, model
                )
                trades.append(trade)
                position = None

        if position is None and np.isfinite(row["Open"]) and np.isfinite(row["PrevSMA21"]):
            if bool(row["LongSignal"]):
                side = "LONG"
                stop = (
                    float(row["Low"])
                    if stop_mode == "entry_bar_extreme"
                    else float(row["Low"])
                )
                if stop_mode == "previous_bar_extreme":
                    if i == 0:
                        stop = np.nan
                    else:
                        stop = float(data.iloc[i - 1]["Low"])
                entry_raw = float(row["Open"])
            elif bool(row["ShortSignal"]):
                side = "SHORT"
                stop = (
                    float(row["High"])
                    if stop_mode == "entry_bar_extreme"
                    else float(row["High"])
                )
                if stop_mode == "previous_bar_extreme":
                    if i == 0:
                        stop = np.nan
                    else:
                        stop = float(data.iloc[i - 1]["High"])
                entry_raw = float(row["Open"])
            else:
                side = None
                stop = np.nan
                entry_raw = np.nan

            if side is not None and np.isfinite(stop):
                qty, _ = position_size(
                    cash, entry_raw, stop, risk_fraction, lot_size
                )
                if qty > 0:
                    entry_fill = adverse_fill(
                        entry_raw, side, is_entry=True, slippage_bps=model.slippage_bps
                    )
                    entry_cost = transaction_cost(
                        entry_fill, qty, side, is_entry=True, model=model
                    )
                    entry_equity = float(cash)

                    if side == "LONG":
                        cash -= entry_fill * qty + entry_cost
                    else:
                        cash += entry_fill * qty - entry_cost

                    position = Position(
                        side=side,
                        entry_date=dt,
                        entry_price=entry_raw,
                        entry_fill=entry_fill,
                        stop=stop,
                        qty=qty,
                        entry_equity=entry_equity,
                        entry_cost=entry_cost,
                    )

                    # Target is the prior-session SMA because the current day's
                    # closing price is not known at today's open.
                    target = float(row["PrevSMA21"])

                    # The literal entry-bar stop is not activated until the next
                    # session. The causal previous-bar stop is active immediately.
                    if stop_mode == "previous_bar_extreme":
                        target_hit, target_fill = _target_hit(row, side, target)
                        stop_hit, stop_fill = _stop_hit(row, side, stop)
                        if stop_hit and target_hit:
                            trade, cash = _close_trade(
                                position, stop_fill, dt, "STOP_ENTRY_DAY_CONSERVATIVE",
                                target, cash, model
                            )
                            trades.append(trade)
                            position = None
                        elif stop_hit:
                            trade, cash = _close_trade(
                                position, stop_fill, dt, "STOP_ENTRY_DAY",
                                target, cash, model
                            )
                            trades.append(trade)
                            position = None
                        elif target_hit:
                            trade, cash = _close_trade(
                                position, target_fill, dt, "SMA_TARGET_ENTRY_DAY",
                                target, cash, model
                            )
                            trades.append(trade)
                            position = None
                    else:
                        target_hit, target_fill = _target_hit(row, side, target)
                        if target_hit:
                            trade, cash = _close_trade(
                                position, target_fill, dt, "SMA_TARGET_ENTRY_DAY",
                                target, cash, model
                            )
                            trades.append(trade)
                            position = None

        if position is None:
            equity = cash
        elif position.side == "LONG":
            equity = cash + position.qty * float(row["Close"])
        else:
            equity = cash - position.qty * float(row["Close"])

        equity_rows.append({"Date": dt, "Equity": float(equity), "Cash": float(cash)})

    if position is not None:
        dt = dates[-1]
        row = data.iloc[-1]
        target = float(row["PrevSMA21"]) if np.isfinite(row["PrevSMA21"]) else np.nan
        trade, cash = _close_trade(
            position, float(row["Close"]), dt, "END_OF_DATA", target, cash, model
        )
        trades.append(trade)
        equity_rows[-1]["Equity"] = float(cash)
        equity_rows[-1]["Cash"] = float(cash)

    trades_df = pd.DataFrame([asdict(x) for x in trades])
    equity_df = pd.DataFrame(equity_rows).set_index("Date")
    result = calculate_metrics(trades_df, equity_df, starting_equity)
    result["NON_CAUSAL_ENTRY_CANDLE_STOP"] = stop_mode == "entry_bar_extreme"
    result["stop_mode"] = stop_mode
    result["target_definition"] = "previous_close_21_sma"
    result["cost_model"] = asdict(model)
    result["signal_diagnostics"] = {
        "rsi_min": float(data["RSI14"].min()) if data["RSI14"].notna().any() else None,
        "rsi_max": float(data["RSI14"].max()) if data["RSI14"].notna().any() else None,
        "rsi_below_10_count": int((data["RSI14"] < 10.0).sum()),
        "rsi_above_90_count": int((data["RSI14"] > 90.0).sum()),
        "gap_down_count": int((data["Open"] < data["PrevClose"]).sum()),
        "gap_up_count": int((data["Open"] > data["PrevClose"]).sum()),
        "long_signal_count": int(data["LongSignal"].sum()),
        "short_signal_count": int(data["ShortSignal"].sum()),
        "sma_valid_rows": int(data["PrevSMA21"].notna().sum()),
    }
    return trades_df, equity_df, result


def monte_carlo_simulation(
    trade_returns: Sequence[float],
    starting_equity: float = 100000.0,
    n_sims: int = 1000,
    seed: int = 42,
    ruin_levels: Iterable[float] = (0.10, 0.20, 0.30, 0.40, 0.50),
) -> tuple[pd.DataFrame, dict, np.ndarray]:
    returns = np.asarray(list(trade_returns), dtype=float)
    returns = returns[np.isfinite(returns)]
    if returns.size == 0:
        raise ValueError("Monte Carlo requires at least one completed trade return.")
    if n_sims <= 0:
        raise ValueError("n_sims must be positive.")
    if np.any(1.0 + returns <= 0.0):
        raise ValueError("Trade returns must be greater than -100% for compounding.")

    rng = np.random.default_rng(seed)

    # Each row is a randomized trade sequence sampled WITH replacement from
    # the historical trade-return distribution. No new market observations
    # are created; only the ordering/composition of observed outcomes changes.
    sampled = rng.choice(returns, size=(n_sims, returns.size), replace=True)

    equity_paths = np.empty((n_sims, returns.size + 1), dtype=float)
    equity_paths[:, 0] = starting_equity
    equity_paths[:, 1:] = starting_equity * np.cumprod(1.0 + sampled, axis=1)

    peaks = np.maximum.accumulate(equity_paths, axis=1)
    drawdowns = equity_paths / peaks - 1.0
    max_drawdowns = drawdowns.min(axis=1)
    final_returns = equity_paths[:, -1] / starting_equity - 1.0

    summary = {
        "n_sims": int(n_sims),
        "n_trades_per_path": int(returns.size),
        "seed": int(seed),
        "final_return_percentiles": {
            str(p): float(np.percentile(final_returns, p))
            for p in [5, 25, 50, 75, 95]
        },
        "max_drawdown_percentiles": {
            str(p): float(np.percentile(max_drawdowns, p))
            for p in [5, 25, 50, 75, 95]
        },
        "risk_of_ruin": {
            f"{int(level * 100)}%": float(np.mean(max_drawdowns <= -level))
            for level in ruin_levels
        },
    }

    distribution = pd.DataFrame(
        {
            "final_return": final_returns,
            "max_drawdown": max_drawdowns,
        }
    )
    return distribution, summary, equity_paths


def plot_monte_carlo(
    equity_paths: np.ndarray,
    output_path: str | Path,
    starting_equity: float,
) -> None:
    fig, ax = plt.subplots(figsize=(12, 7))
    for path in equity_paths:
        ax.plot(path, alpha=0.03, linewidth=0.7)
    ax.axhline(
        starting_equity,
        linestyle="--",
        linewidth=1.0,
        label="Starting equity",
    )
    ax.set_title("Monte Carlo Equity Curves - Bootstrap With Replacement")
    ax.set_xlabel("Completed trades")
    ax.set_ylabel("Equity (INR)")
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def vectorbt_reconciliation(
    data: pd.DataFrame,
    trades: pd.DataFrame,
    starting_equity: float,
) -> dict:
    try:
        import vectorbt as vbt
    except Exception as exc:
        return {"available": False, "reason": repr(exc)}

    if trades.empty:
        return {"available": True, "trade_count": 0}

    entry_dates = pd.to_datetime(trades["entry_date"])
    exit_dates = pd.to_datetime(trades["exit_date"])
    if (entry_dates == exit_dates).any():
        return {
            "available": True,
            "reconciled": False,
            "reconciliation_error": (
                "Same-day round trips cannot be faithfully represented by one "
                "daily order-price slot; the primary event-driven ledger remains authoritative."
            ),
        }

    all_order_dates = pd.Index(entry_dates.tolist() + exit_dates.tolist())
    if all_order_dates.duplicated().any():
        return {
            "available": True,
            "reconciled": False,
            "reconciliation_error": (
                "Multiple orders share a daily timestamp; vectorbt reconciliation "
                "requires intraday order prices."
            ),
        }

    orders = pd.DataFrame(0.0, index=data.index, columns=["size", "price"])
    for _, trade in trades.iterrows():
        entry_date = pd.Timestamp(trade["entry_date"])
        exit_date = pd.Timestamp(trade["exit_date"])
        qty = float(trade["qty"])
        entry_size, exit_size = (
            (qty, -qty) if trade["side"] == "LONG" else (-qty, qty)
        )
        orders.loc[entry_date, ["size", "price"]] = [entry_size, float(trade["entry_fill"])]
        orders.loc[exit_date, ["size", "price"]] = [exit_size, float(trade["exit_fill"])]

    try:
        pf = vbt.Portfolio.from_orders(
            close=data["Close"],
            size=orders["size"],
            price=orders["price"].replace(0.0, np.nan),
            direction="both",
            init_cash=starting_equity,
            fees=0.0,
            slippage=0.0,
            freq="1D",
        )
        return {
            "available": True,
            "final_value": float(pf.value().iloc[-1]),
            "total_return": float(pf.total_return()),
        }
    except Exception as exc:
        return {"available": True, "reconciliation_error": repr(exc)}


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Daily RSI/SMA gap-reversion backtest plus Monte Carlo"
    )
    parser.add_argument("--ticker", default="^NSEI")
    parser.add_argument("--start", default="2010-01-01")
    parser.add_argument("--end", default=None)
    parser.add_argument("--starting-equity", type=float, default=100000.0)
    parser.add_argument("--risk-fraction", type=float, default=0.01)
    parser.add_argument("--lot-size", type=int, default=1)
    parser.add_argument(
        "--stop-mode",
        choices=["entry_bar_extreme", "previous_bar_extreme"],
        default="entry_bar_extreme",
    )
    parser.add_argument("--n-mc", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--refresh-data", action="store_true")
    parser.add_argument("--data-cache-dir", default="data/raw")
    parser.add_argument("--output-dir", default="results")
    parser.add_argument("--slippage-bps", type=float, default=5.0)
    parser.add_argument("--brokerage-per-order", type=float, default=20.0)
    parser.add_argument("--exchange-txn-rate", type=float, default=0.0)
    parser.add_argument("--stt-buy-rate", type=float, default=0.0)
    parser.add_argument("--stt-sell-rate", type=float, default=0.0)
    parser.add_argument("--stamp-buy-rate", type=float, default=0.0)
    parser.add_argument("--gst-rate", type=float, default=0.18)
    parser.add_argument("--sebi-turnover-rate", type=float, default=0.0)
    return parser


def main() -> None:
    args = build_arg_parser().parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    costs = CostModel(
        slippage_bps=args.slippage_bps,
        brokerage_per_order=args.brokerage_per_order,
        exchange_txn_rate=args.exchange_txn_rate,
        stt_buy_rate=args.stt_buy_rate,
        stt_sell_rate=args.stt_sell_rate,
        stamp_buy_rate=args.stamp_buy_rate,
        gst_rate=args.gst_rate,
        sebi_turnover_rate=args.sebi_turnover_rate,
    )

    data = fetch_daily_data(
        ticker=args.ticker,
        start=args.start,
        end=args.end,
        cache_dir=args.data_cache_dir,
        refresh=args.refresh_data,
    )

    trades, equity, metrics = run_backtest(
        data,
        starting_equity=args.starting_equity,
        risk_fraction=args.risk_fraction,
        lot_size=args.lot_size,
        costs=costs,
        stop_mode=args.stop_mode,
    )

    if trades.empty:
        mc_summary = {
            "status": "not_run",
            "reason": "No completed trades were generated.",
        }
        mc_distribution = pd.DataFrame()
    else:
        mc_distribution, mc_summary, paths = monte_carlo_simulation(
            trades["return_on_equity"].to_numpy(),
            starting_equity=args.starting_equity,
            n_sims=args.n_mc,
            seed=args.seed,
        )
        plot_monte_carlo(
            paths,
            output_dir / "monte_carlo_equity_curves.png",
            args.starting_equity,
        )
        mc_distribution.to_csv(
            output_dir / "monte_carlo_distribution.csv", index=False
        )

    trades.to_csv(output_dir / "trades.csv", index=False)
    equity.to_csv(output_dir / "equity_curve.csv")

    cache_path = Path(args.data_cache_dir) / f"{safe_name(args.ticker)}.csv"
    metrics["research_manifest"] = {
        "git_sha": current_git_sha(),
        "ticker": args.ticker,
        "start": args.start,
        "end": args.end,
        "data_cache_file": str(cache_path),
        "data_sha256": sha256_file(cache_path),
        "data_rows": int(len(data)),
        "data_first_date": str(data.index.min().date()),
        "data_last_date": str(data.index.max().date()),
        "starting_equity": args.starting_equity,
        "risk_fraction": args.risk_fraction,
        "lot_size": args.lot_size,
        "stop_mode": args.stop_mode,
        "target_definition": "previous_close_21_sma",
        "monte_carlo_paths": args.n_mc,
        "monte_carlo_seed": args.seed,
    }

    (output_dir / "backtest_metrics.json").write_text(
        json.dumps(metrics, indent=2, default=str),
        encoding="utf-8",
    )
    (output_dir / "monte_carlo_summary.json").write_text(
        json.dumps(mc_summary, indent=2, default=str),
        encoding="utf-8",
    )
    (output_dir / "vectorbt_reconciliation.json").write_text(
        json.dumps(
            vectorbt_reconciliation(data, trades, args.starting_equity),
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )

    print(json.dumps(metrics, indent=2, default=str))
    print(json.dumps(mc_summary, indent=2, default=str))
    print(f"Artifacts: {output_dir.resolve()}")
    if args.stop_mode == "entry_bar_extreme":
        print(
            "WARNING: entry-bar low/high sizing is NON-CAUSAL with daily OHLC. "
            "Use previous_bar_extreme or intraday data for causal research."
        )


if __name__ == "__main__":
    main()
