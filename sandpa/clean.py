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
    # TODO (Block 3, step 1)
    raise NotImplementedError


def clean_prices(df: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy of df. Don't change df itself.

    - date converted to pandas datetime
    - sorted by date, oldest first
    - duplicate dates removed (keep the first)
    - rows with a missing value in PRICE_FIELDS dropped
    - fresh 0..n-1 index
    """
    # TODO (Block 3, step 2)
    raise NotImplementedError
