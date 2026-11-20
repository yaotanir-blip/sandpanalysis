"""Block 3: check the data before trusting any result.

Your 2023-24 Year 1-5 files had day and month swapped on some rows and prices stored as text.
These checks would have caught that. tests/test_clean.py says when they're done.
"""

from __future__ import annotations

import pandas as pd

PRICE_FIELDS = ["open", "high", "low", "close", "adj_close"]


def find_problems(df: pd.DataFrame, max_move: float = 0.2, max_gap_days: int = 5) -> list[str]:
    """Return a list of readable problem descriptions. An empty list means the data looks fine.

    Detect each of these (each message must contain the word in quotes):
    - dates not in increasing order                              -> "order"
    - the same date appearing more than once                     -> "duplicate"
    - missing values in any of PRICE_FIELDS                      -> "missing"
    - a price of zero or below in any of PRICE_FIELDS            -> "non-positive"
    - a day-to-day change in adj_close bigger than max_move      -> "large move"
      (0.2 = 20% up or down)
    - more than max_gap_days calendar days between two rows      -> "gap"
      (weekends give 3 days and holidays 4, so 5 is a safe default)
    Say where the problem is (e.g. the date) so you can go and look.
    """
    problems = []
    dates = pd.to_datetime(df["date"])           # real dates, so you can compare and subtract them

    # 1. "order": every date should be later than the one before it
    if not dates.is_monotonic_increasing:
        problems.append("dates are not in increasing order")

    # 2. "duplicate"
    dupes = dates.duplicated()                   # True where a date has already appeared
    if dupes.any():
        problems.append(f"duplicate dates: {df.loc[dupes, 'date'].tolist()}")

    # 3. "missing": a gap in any price column
    missing = df[PRICE_FIELDS].isna().any(axis=1)   # True if any price on that row is empty
    if missing.any():
        problems.append(f"missing prices: {df.loc[missing,'date'].tolist()}")                                             # same pattern as 2

    # 4. "non-positive": a price of 0 or below
    bad = (df[PRICE_FIELDS]<=0).any(axis=1)                                       # like 3, but compare with <= 0 instead of isna()
    if bad.any():
        problems.append(f"non-positive prices:{df.loc[bad,'date'].tolist()}")

    # 5. "large move": daily change in adj_close bigger than max_move
    change = df["adj_close"] / df["adj_close"].shift(1) - 1   # shift(1) = the previous row
    big = change.abs()>max_move
    if big.any():
        problems.append(f"large move on: {df.loc[big,'date'].tolist()}")                                       # use .abs(), so falls count as well as rises
    

    # 6. "gap": more than max_gap_days between two rows
    gap_days = dates.diff().dt.days                 # days since the previous row
    gap = gap_days>max_gap_days
    if gap.any():
        problems.append(f"gap days on: {df.loc[gap,'date'].tolist()}")

    return problems


def clean_prices(df: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy of df. Don't change df itself.

    - date converted to pandas datetime
    - sorted by date, oldest first
    - duplicate dates removed (keep the first)
    - rows with a missing value in PRICE_FIELDS dropped
    - fresh 0..n-1 index
    """
    out = df.copy()                     # never change the table you were given
    out["date"] = pd.to_datetime(df["date"])                    # convert to real dates (as in step 1)
    out = out.sort_values('date',ascending=True)                           # sort by date
    out = out.drop_duplicates(subset="date",keep="first")                           # drop_duplicates(subset="date", keep="first")
    out = out.dropna(subset=PRICE_FIELDS)                           # dropna(subset=PRICE_FIELDS)
    return out.reset_index(drop=True)
