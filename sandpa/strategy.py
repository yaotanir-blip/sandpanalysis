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
    change = prices / prices.shift(1) - 1 
    return change


def streak_lengths(returns: pd.Series) -> tuple[list[int], list[int]]:
    """Lengths of consecutive runs of up days (r > 0) and down days (r < 0).

    Returns (up_lengths, down_lengths), each in the order the runs happen.
    A NaN or a return of exactly 0 ends the current run and isn't counted itself.
    The run still going on the last day counts.
    """
    up_lengths, down_lengths = [], []
    up = down = 0                        # length of the current up run and down run

    for r in returns:
        if r > 0:                        # an up day
            if down > 0:                 # so a down run has just ended: save it
                down_lengths.append(down)
                down = 0
            up += 1
        elif r < 0:                      # a down day
            if up > 0:
                up_lengths.append(up)
                up = 0
            down += 1                          # the mirror image of the branch above
        else:                            # NaN or exactly 0: ends whatever run is going
            if up >0:
                up_lengths.append(up)
            if down > 0:
                down_lengths.append(down)
            up = down = 0                          # save any run that's going, then reset both to 0

    # the run still going on the last day counts too
    if up >0:
        up_lengths.append(up)
    if down > 0:
        down_lengths.append(down)                                  # same as the else branch
    return up_lengths, down_lengths


def average_streaks(returns: pd.Series) -> tuple[float, float]:
    """(average up-run length, average down-run length). Use 0.0 when there are no runs."""
    up_lengths, down_lengths = streak_lengths(returns)
    avg_up = sum(up_lengths) / len(up_lengths) if up_lengths else 0.0
    avg_down = sum(down_lengths) / len(down_lengths) if down_lengths else 0.0                       # the same for down_lengths
    return avg_up, avg_down


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
    returns = daily_returns(prices)
    cash = start_cash
    shares = 0.0
    buy_price = None
    up = down = 0
    equity = []                    # portfolio value at each day's close
    trades = []                    # one tuple per trade: (date, action, price, value_after)

    for date, price, r in zip(prices.index, prices, returns):
        # 1. Update the current runs (simpler than streak_lengths: just the counts)
        if r > 0:
            up += 1
            down = 0
        elif r < 0:
            down += 1 
            up = 0 
        else:
            up = down = 0

        # 2. At most one trade per day, so use if / elif / elif
        if shares == 0 and down >= buy_after:
            shares = cash * (1-cost)/price         # cash * (1 - cost) / price
            cash = 0.0
            buy_price = price
            trades.append((date, "buy", price, shares * price))
        elif shares > 0 and stop_loss is not None and price <= buy_price * (1-stop_loss):   # buy_price * (1 - stop_loss)
            cash = shares * price * (1-cost)             # shares * price * (1 - cost)
            shares = 0.0
            trades.append((date, "stop_loss", price, cash))
        elif shares > 0 and up >= sell_after:
            cash = shares * price * (1-cost)
            shares = 0.0
            trades.append((date,"sell",price,cash))
                                # like the stop-loss branch, but the action is "sell"

        # 3. Record today's value
        equity.append(cash + shares * price)         # cash + shares * price

    equity = pd.Series(equity, index=prices.index)
    trades = pd.DataFrame(trades, columns=["date", "action", "price", "value_after"])
    return equity, trades


def buy_and_hold(prices: pd.Series, cost: float = 0.0, start_cash: float = 1000.0) -> pd.Series:
    """The benchmark: buy at the first close (paying cost as above) and never sell.

    Returns equity with the same index as prices.
    """
    shares = start_cash * (1-cost)/prices.iloc[0]
    return prices * shares
