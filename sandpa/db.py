"""Block 2: store prices in SQLite and read them back with SQL.

You write create_table, save_prices and load_prices. tests/test_db.py says when they're done.
"""

from __future__ import annotations

import sqlite3

import pandas as pd

from sandpa import PRICE_COLUMNS


def connect(db_path) -> sqlite3.Connection:
    """Open (or create) the database file. Use ':memory:' for a throwaway database."""
    return sqlite3.connect(str(db_path))


def create_table(conn: sqlite3.Connection) -> None:
    """Create the `prices` table if it doesn't already exist.

    - One column per name in PRICE_COLUMNS, with sensible types (TEXT, REAL, INTEGER).
    - (symbol, date) is the PRIMARY KEY, so the same day can't be stored twice.
    - Calling it twice must not fail.
    """
    # TODO (Block 2, step 1)
    raise NotImplementedError


def save_prices(conn: sqlite3.Connection, df: pd.DataFrame) -> int:
    """Insert the rows of df (columns = PRICE_COLUMNS) into `prices`.

    - Skip rows that are already stored (same symbol and date) instead of failing.
    - Use ? placeholders for values, never f-strings (look up "SQL injection").
    - Commit, then return how many new rows were actually inserted.
    """
    # TODO (Block 2, step 2)
    raise NotImplementedError


def load_prices(
    conn: sqlite3.Connection,
    symbol: str,
    start_date: str | None = None,
    end_date: str | None = None,
) -> pd.DataFrame:
    """Return the stored rows for one symbol as a DataFrame.

    - Columns = PRICE_COLUMNS, oldest date first.
    - start_date / end_date ('YYYY-MM-DD') are optional and inclusive.
    - Do the filtering and sorting in SQL (WHERE, ORDER BY), not in pandas.
    """
    # TODO (Block 2, step 3)
    raise NotImplementedError
