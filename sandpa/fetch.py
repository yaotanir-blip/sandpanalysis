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
        # 1. Defaults
    if session is None:
        session = requests.Session()         # a real requests.Session()
    if api_key is None:
        api_key = config.get_api_key()          # from config

    # 2. Build the request (same as explore_api.py, but using the function's inputs)
    url = f"{config.API_BASE_URL}/{symbol}/prices"
    params = {"startDate":start_date}
    if end_date is not None:
        params["endDate"]=end_date
    headers = {"Authorization":f"Token {api_key}"}

    # 3. Up to max_retries attempts
    for attempt in range(max_retries):          # attempt = 0, 1, 2, ...
        try:
            response = session.get(url, params=params, headers=headers, timeout=timeout)
        except (requests.Timeout, requests.ConnectionError) as err:
            log.warning('Attempt %d failed: %s',attempt+1,err)                    # which attempt failed, and err
        else:                                   # runs only if no exception happened
            # 4. Decide based on the status code
            if response.status_code == 200:
                return response.json()
            if response.status_code not in RETRY_STATUS_CODES:
                raise FetchError(f'Failed with status{response.status_code}:{response.text}')           # include the status code and response.text
            log.warning('Attempt %d got status %d, retrying',attempt+1,response.status_code)                    # a retryable status: say which one

        # 5. Wait before the next attempt: backoff * 2 ** attempt seconds
        time.sleep(backoff * 2** attempt)

    # 6. Every attempt failed
    raise FetchError(f'Gave up after {max_retries} attempts')

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

    if not rows:
        return pd.DataFrame(columns=PRICE_COLUMNS)
    df = pd.DataFrame(rows)
    df = df.rename(columns={"adjClose": "adj_close"})
    df["symbol"] = symbol
    df["date"] = df["date"].str[:10]
    price_cols = ["open", "high", "low", "close", "adj_close"]
    df[price_cols] = df[price_cols].astype(float)
    df["volume"] = df["volume"].astype(int)
    df = df[PRICE_COLUMNS]
    df = df.sort_values("date").reset_index(drop=True)
    return df
