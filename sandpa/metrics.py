from __future__ import annotations

import pandas as pd


def total_return(equity: pd.Series) -> float:
    """Last value / first value - 1 (0.3 means +30%)."""
    return equity.iloc[-1]/equity.iloc[0] -1 


def annualised_return(equity: pd.Series, trading_days: int = 252) -> float:
    """Total return turned into a yearly rate: (1 + total) ** (trading_days / (n - 1)) - 1,
    where n is the number of values in equity."""
    years = (len(equity)-1)/trading_days
    return (1+total_return(equity)) ** (1/years)-1


def max_drawdown(equity: pd.Series) -> float:
    """Largest fall from a previous peak, as a negative fraction (-0.25 means -25%). 0.0 if it never falls."""
    peak = equity.cummax()
    drawdown = equity /peak-1
    return float(drawdown.min())


def summary(equity: pd.Series, trades: pd.DataFrame | None = None) -> dict:
    """Dict with keys total_return, annualised_return, max_drawdown, n_trades.
    n_trades = number of rows in trades (0 if trades is None)."""
    return {"total_return": total_return(equity),"annualised_return":annualised_return(equity),"max_drawdown":max_drawdown(equity),"n_trades":0 if trades is None else len(trades)}
