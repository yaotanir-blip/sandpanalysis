"""Block 5: numbers that let you compare the strategy with buy-and-hold fairly.

tests/test_metrics.py says when they're done.
"""

from __future__ import annotations

import pandas as pd


def total_return(equity: pd.Series) -> float:
    """Last value / first value - 1 (0.3 means +30%)."""
    # TODO (Block 5, step 1)
    raise NotImplementedError


def annualised_return(equity: pd.Series, trading_days: int = 252) -> float:
    """Total return turned into a yearly rate: (1 + total) ** (trading_days / (n - 1)) - 1,
    where n is the number of values in equity."""
    # TODO (Block 5, step 1)
    raise NotImplementedError


def max_drawdown(equity: pd.Series) -> float:
    """Largest fall from a previous peak, as a negative fraction (-0.25 means -25%). 0.0 if it never falls."""
    # TODO (Block 5, step 1)
    raise NotImplementedError


def summary(equity: pd.Series, trades: pd.DataFrame | None = None) -> dict:
    """Dict with keys total_return, annualised_return, max_drawdown, n_trades.
    n_trades = number of rows in trades (0 if trades is None)."""
    # TODO (Block 5, step 1)
    raise NotImplementedError
