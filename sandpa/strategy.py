"""Block 4: the streak strategy from 2023-24, with its rules written down precisely.

You write every function here. tests/test_strategy.py says when they're done.
Assumption to mention in the README: trades happen at the close of the day the signal appears.
"""

from __future__ import annotations

import pandas as pd


def daily_returns(prices: pd.Series) -> pd.Series:
    """Fractional change from one day to the next: r_t = p_t / p_(t-1) - 1.

    Same index as prices. The first value is NaN.
    """
    # TODO (Block 4, step 1)
    raise NotImplementedError


def streak_lengths(returns: pd.Series) -> tuple[list[int], list[int]]:
    """Lengths of consecutive runs of up days (r > 0) and down days (r < 0).

    Returns (up_lengths, down_lengths), each in the order the runs happen.
    A NaN or a return of exactly 0 ends the current run and isn't counted itself.
    The run still going on the last day counts.
    """
    # TODO (Block 4, step 2)
    raise NotImplementedError


def average_streaks(returns: pd.Series) -> tuple[float, float]:
    """(average up-run length, average down-run length). Use 0.0 when there are no runs."""
    # TODO (Block 4, step 2)
    raise NotImplementedError


def backtest_streaks(
    prices: pd.Series,
    buy_after: float,
    sell_after: float,
    stop_loss: float | None = None,
    cost: float = 0.0,
    start_cash: float = 1000.0,
) -> tuple[pd.Series, pd.DataFrame]:
    """Simulate the streak strategy on daily closing prices (index = dates).

    Rules:
    - Track the current run of down days and of up days, as in streak_lengths.
    - At most one trade per day.
    - Not invested and the down run is >= buy_after: buy at today's close with all your cash.
    - Invested, stop_loss is set and close <= buy_price * (1 - stop_loss):
      sell at today's close, action 'stop_loss'. Check this before the next rule.
    - Invested and the up run is >= sell_after: sell at today's close, action 'sell'.
    - Costs: buying spends all cash, the fee is cost * cash, the rest buys shares
      (shares = cash * (1 - cost) / price). Selling gives cash = shares * price * (1 - cost).
    - Still invested on the last day: value the shares at the last close (don't sell).

    Returns:
    - equity: Series with the same index as prices: cash + shares * close at each day's close
    - trades: DataFrame with columns date, action ('buy', 'sell' or 'stop_loss'), price, value_after
    """
    # TODO (Block 4, step 3)
    raise NotImplementedError


def buy_and_hold(prices: pd.Series, cost: float = 0.0, start_cash: float = 1000.0) -> pd.Series:
    """The benchmark: buy at the first close (paying cost as above) and never sell.

    Returns equity with the same index as prices.
    """
    # TODO (Block 4, step 4)
    raise NotImplementedError
