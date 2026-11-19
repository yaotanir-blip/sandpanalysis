"""Tests for Block 4. Run with:  pytest tests/test_strategy.py -v

The prices here are tiny on purpose, so you can work out every answer by hand.
"""

import math

import pandas as pd
import pytest

from sandpa.strategy import (
    average_streaks,
    backtest_streaks,
    buy_and_hold,
    daily_returns,
    streak_lengths,
)


def series(values):
    return pd.Series(values, index=pd.date_range("2024-01-01", periods=len(values), freq="D"), dtype=float)


# ---------- returns and streaks ----------

def test_daily_returns():
    r = daily_returns(series([100, 110, 99]))
    assert math.isnan(r.iloc[0])
    assert r.iloc[1] == pytest.approx(0.10)
    assert r.iloc[2] == pytest.approx(-0.10)


def test_streak_lengths():
    r = daily_returns(series([100, 101, 102, 101, 100, 99, 100]))  # up up down down down up
    assert streak_lengths(r) == ([2, 1], [3])


def test_zero_return_ends_a_run():
    r = daily_returns(series([100, 101, 101, 102]))  # up, flat, up
    assert streak_lengths(r) == ([1, 1], [])


def test_average_streaks():
    r = daily_returns(series([100, 101, 102, 101, 100, 99, 100]))
    assert average_streaks(r) == (pytest.approx(1.5), pytest.approx(3.0))


def test_average_streaks_with_no_down_days():
    r = daily_returns(series([100, 101, 102]))
    assert average_streaks(r) == (pytest.approx(2.0), 0.0)


# ---------- backtest ----------

def test_buy_then_sell():
    prices = series([100, 99, 98, 99, 100, 101])
    equity, trades = backtest_streaks(prices, buy_after=2, sell_after=2)

    assert trades["action"].tolist() == ["buy", "sell"]
    assert trades["price"].tolist() == [98, 100]
    assert list(equity.index) == list(prices.index)
    expected = [1000, 1000, 1000, 1000 * 99 / 98, 1000 * 100 / 98, 1000 * 100 / 98]
    assert equity.tolist() == pytest.approx(expected)


def test_costs_are_paid_on_both_trades():
    prices = series([100, 99, 98, 99, 100, 101])
    equity, _ = backtest_streaks(prices, buy_after=2, sell_after=2, cost=0.01)
    assert equity.iloc[-1] == pytest.approx(1000 * 0.99 * (100 / 98) * 0.99)


def test_stop_loss_losses_are_counted():
    # The 2024 script forgot to update its running value after a stop-loss sale.
    prices = series([100, 99, 98, 95, 96, 97])
    equity, trades = backtest_streaks(prices, buy_after=2, sell_after=2, stop_loss=0.02)

    assert trades["action"].tolist() == ["buy", "stop_loss"], "one trade per day: no re-buy on the stop-loss day"
    assert equity.iloc[-1] == pytest.approx(1000 * 95 / 98)


def test_still_invested_at_the_end():
    prices = series([100, 99, 98, 97])
    equity, trades = backtest_streaks(prices, buy_after=2, sell_after=2)
    assert trades["action"].tolist() == ["buy"]
    assert equity.iloc[-1] == pytest.approx(1000 * 97 / 98)


def test_trades_table_columns():
    _, trades = backtest_streaks(series([100, 99, 98, 99, 100]), buy_after=2, sell_after=2)
    assert list(trades.columns) == ["date", "action", "price", "value_after"]


# ---------- benchmark ----------

def test_buy_and_hold():
    assert buy_and_hold(series([100, 110, 99])).tolist() == pytest.approx([1000, 1100, 990])


def test_buy_and_hold_with_cost():
    assert buy_and_hold(series([100, 110, 99]), cost=0.01).tolist() == pytest.approx([990, 1089, 980.1])
