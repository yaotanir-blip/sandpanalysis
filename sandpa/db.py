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
    conn.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            symbol    TEXT,
            date      TEXT,
            open      REAL,
            high      REAL,
            low       REAL,
            close     REAL,
            adj_close REAL,
            volume    INTEGER,
            PRIMARY KEY (symbol, date)
        )
    """)


def save_prices(conn: sqlite3.Connection, df: pd.DataFrame) -> int:
    """Insert the rows of df (columns = PRICE_COLUMNS) into `prices`.

    - Skip rows that are already stored (same symbol and date) instead of failing.
    - Use ? placeholders for values, never f-strings (look up "SQL injection").
    - Commit, then return how many new rows were actually inserted.
    """
    sql = "INSERT OR IGNORE INTO prices VALUES(?,?,?,?,?,?,?,?)"                                                    # see below
    rows = df[PRICE_COLUMNS].itertuples(index=False, name=None)  # each row as a plain tuple
    cursor = conn.executemany(sql, rows)                         # runs the SQL once per row
    conn.commit()
    return cursor.rowcount                                                   # see below


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
    sql = "SELECT * FROM prices WHERE symbol = ?"
    values = [symbol]
    if start_date is not None:
        sql += " AND date >= ?"
        values.append(start_date)
    if end_date is not None:
        sql += "AND date <= ?"
        values.append(end_date)                          # the same idea, but with <=
    sql += " ORDER BY date"           # which column? oldest first is the default order
    df = pd.read_sql_query(sql, conn, params=values)
    return df[PRICE_COLUMNS]
