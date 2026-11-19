"""Block 1: get daily prices from the Tiingo API.

You write the two functions below. tests/test_fetch.py says when they're done.
"""

from __future__ import annotations

import logging
import time

import pandas as pd
import requests

from sandpa import PRICE_COLUMNS, config

log = logging.getLogger(__name__)

# Status codes worth trying again: 429 = rate limited, 5xx = server problem
RETRY_STATUS_CODES = {429, 500, 502, 503, 504}


class FetchError(Exception):
    """Raised when prices can't be fetched."""


def fetch_prices(
    symbol: str,
    start_date: str,
    end_date: str | None = None,
    api_key: str | None = None,
    session=None,
    max_retries: int = 3,
    timeout: float = 10,
    backoff: float = 1.0,
) -> list[dict]:
    """Request daily prices for one symbol and return the API's JSON rows.

    Rules (the tests check these):
    - Send a GET request to f"{config.API_BASE_URL}/{symbol}/prices"
      with startDate (and endDate, if given) as query parameters.
    - Authenticate with api_key (use config.get_api_key() if it's None).
      Check Tiingo's docs for how the key should be sent.
    - Always pass timeout=timeout, so a dead connection can't hang forever.
    - Status 200: return response.json().
    - Status in RETRY_STATUS_CODES, or a requests.Timeout / requests.ConnectionError:
      log a warning, wait backoff * 2**attempt seconds, and try again.
      Make at most max_retries attempts in total.
    - Any other status (e.g. 401 wrong key, 404 unknown ticker): don't retry.
      Raise FetchError with the status code and response text in the message.
    - If every attempt fails: raise FetchError.

    `session` lets the tests pass a fake object with a .get() method.
    If it's None, use requests.Session().
    """
    # TODO (Block 1, step 3)
    raise NotImplementedError


def parse_prices(rows: list[dict], symbol: str) -> pd.DataFrame:
    """Turn the API's JSON rows into a tidy DataFrame.

    Output columns, exactly and in this order: PRICE_COLUMNS
        symbol, date, open, high, low, close, adj_close, volume
    - symbol: the symbol passed in, on every row
    - date: a string 'YYYY-MM-DD' (the API's dates include a time part: drop it)
    - open, high, low, close, adj_close: floats; volume: int
    - sorted by date, oldest first, with a fresh 0..n-1 index
    An empty list gives an empty DataFrame with the same columns.

    Look at tests/fixtures/sample_response.json to see the API's field names.
    """
    # TODO (Block 1, step 2)
    raise NotImplementedError
