"""Tests for Block 2. Run with:  pytest tests/test_db.py -v"""

import pandas as pd
import pytest

from sandpa import PRICE_COLUMNS
from sandpa.db import connect, create_table, load_prices, save_prices


def make_prices(symbol, dates):
    return pd.DataFrame(
        {
            "symbol": symbol,
            "date": dates,
            "open": 100.0,
            "high": 101.0,
            "low": 99.0,
            "close": 100.5,
            "adj_close": 100.5,
            "volume": 1_000_000,
        }
    )[PRICE_COLUMNS]


@pytest.fixture
def conn():
    c = connect(":memory:")
    create_table(c)
    yield c
    c.close()


def test_create_table_twice_is_fine(conn):
    create_table(conn)


def test_save_counts_new_rows_and_skips_duplicates(conn):
    first = make_prices("SPY", ["2024-01-03", "2024-01-02", "2024-01-04"])
    assert save_prices(conn, first) == 3
    assert save_prices(conn, first) == 0, "saving the same rows again should insert nothing"

    overlap = make_prices("SPY", ["2024-01-04", "2024-01-05"])
    assert save_prices(conn, overlap) == 1


def test_load_is_sorted_with_the_right_columns(conn):
    save_prices(conn, make_prices("SPY", ["2024-01-04", "2024-01-02", "2024-01-03"]))
    df = load_prices(conn, "SPY")
    assert list(df.columns) == PRICE_COLUMNS
    assert df["date"].tolist() == ["2024-01-02", "2024-01-03", "2024-01-04"]


def test_load_filters_by_symbol_and_dates(conn):
    save_prices(conn, make_prices("SPY", ["2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"]))
    save_prices(conn, make_prices("QQQ", ["2024-01-03"]))

    df = load_prices(conn, "SPY", start_date="2024-01-03", end_date="2024-01-04")
    assert df["date"].tolist() == ["2024-01-03", "2024-01-04"], "date filters are inclusive"
    assert (df["symbol"] == "SPY").all()
