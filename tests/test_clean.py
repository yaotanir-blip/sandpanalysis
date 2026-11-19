"""Tests for Block 3. Run with:  pytest tests/test_clean.py -v"""

import numpy as np
import pandas as pd

from sandpa.clean import clean_prices, find_problems


def make(dates, closes):
    return pd.DataFrame(
        {
            "symbol": "SPY",
            "date": dates,
            "open": closes,
            "high": closes,
            "low": closes,
            "close": closes,
            "adj_close": closes,
            "volume": 1_000_000,
        }
    )


GOOD_DATES = ["2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05", "2024-01-08"]
GOOD_CLOSES = [100.0, 101.0, 100.5, 102.0, 101.5]


def has(problems, word):
    return any(word in p.lower() for p in problems)


def test_good_data_has_no_problems():
    assert find_problems(make(GOOD_DATES, GOOD_CLOSES)) == []


def test_day_month_swap_breaks_the_order():
    # Like your old Year 1 file: 1 Aug 2024 stored as 8 Jan 2024
    dates = ["2024-07-30", "2024-07-31", "2024-01-08", "2024-08-02"]
    assert has(find_problems(make(dates, [100.0, 101.0, 102.0, 103.0])), "order")


def test_duplicate_dates():
    dates = ["2024-01-02", "2024-01-03", "2024-01-03", "2024-01-04"]
    assert has(find_problems(make(dates, [100.0, 101.0, 101.0, 102.0])), "duplicate")


def test_missing_values():
    closes = [100.0, np.nan, 100.5, 102.0, 101.5]
    assert has(find_problems(make(GOOD_DATES, closes)), "missing")


def test_non_positive_price():
    closes = [100.0, 0.0, 100.5, 102.0, 101.5]
    assert has(find_problems(make(GOOD_DATES, closes)), "non-positive")


def test_large_move():
    closes = [100.0, 130.0, 131.0, 130.5, 131.5]
    assert has(find_problems(make(GOOD_DATES, closes)), "large move")


def test_gap():
    dates = ["2024-01-02", "2024-01-03", "2024-01-15", "2024-01-16", "2024-01-17"]
    assert has(find_problems(make(dates, GOOD_CLOSES)), "gap")


def test_clean_sorts_dedupes_and_drops_missing():
    raw = make(
        ["2024-01-04", "2024-01-02", "2024-01-03", "2024-01-03", "2024-01-05"],
        [102.0, 100.0, 101.0, 101.0, np.nan],
    )
    before = raw.copy()
    out = clean_prices(raw)

    pd.testing.assert_frame_equal(raw, before)  # input not changed
    assert pd.api.types.is_datetime64_any_dtype(out["date"])
    assert out["date"].dt.strftime("%Y-%m-%d").tolist() == ["2024-01-02", "2024-01-03", "2024-01-04"]
    assert list(out.index) == [0, 1, 2]
