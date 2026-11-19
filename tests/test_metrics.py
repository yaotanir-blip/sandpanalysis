"""Tests for Block 5. Run with:  pytest tests/test_metrics.py -v"""

import pandas as pd
import pytest

from sandpa.metrics import annualised_return, max_drawdown, summary, total_return

EQUITY = pd.Series([100.0, 120.0, 90.0, 130.0])


def test_total_return():
    assert total_return(EQUITY) == pytest.approx(0.30)


def test_annualised_return():
    # 3 steps between 4 values; with trading_days=3 one "year" has passed
    assert annualised_return(EQUITY, trading_days=3) == pytest.approx(0.30)


def test_max_drawdown():
    assert max_drawdown(EQUITY) == pytest.approx(-0.25)  # 120 -> 90


def test_no_drawdown():
    assert max_drawdown(pd.Series([100.0, 110.0, 120.0])) == 0.0


def test_summary():
    trades = pd.DataFrame({"date": [1, 2], "action": ["buy", "sell"], "price": [1, 2], "value_after": [1, 2]})
    s = summary(EQUITY, trades)
    assert set(s) == {"total_return", "annualised_return", "max_drawdown", "n_trades"}
    assert s["n_trades"] == 2
    assert summary(EQUITY)["n_trades"] == 0
