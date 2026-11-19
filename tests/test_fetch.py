"""Tests for Block 1. Run with:  pytest tests/test_fetch.py -v"""

import json
from pathlib import Path

import pandas as pd
import pytest
import requests

from sandpa import PRICE_COLUMNS
from sandpa.fetch import FetchError, fetch_prices, parse_prices

FIXTURE = Path(__file__).parent / "fixtures" / "sample_response.json"


# ---------- fakes, so the tests never touch the real API ----------

class FakeResponse:
    def __init__(self, status_code, data=None, text=""):
        self.status_code = status_code
        self._data = data
        self.text = text or json.dumps(data)

    @property
    def ok(self):
        return self.status_code < 400

    def json(self):
        return self._data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} error", response=self)


class FakeSession:
    """Returns (or raises) the given outcomes in order and records every call."""

    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.calls = []

    def get(self, url, **kwargs):
        self.calls.append((url, kwargs))
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


ROWS = [{"date": "2024-01-02T00:00:00.000Z", "close": 100.0}]


def call(session, **kwargs):
    return fetch_prices("SPY", "2024-01-01", api_key="test-key", session=session, backoff=0, **kwargs)


# ---------- fetch_prices ----------

def test_success_returns_json_and_sets_timeout():
    session = FakeSession([FakeResponse(200, ROWS)])
    assert call(session) == ROWS
    url, kwargs = session.calls[0]
    assert "/SPY/prices" in url
    assert "timeout" in kwargs, "always pass a timeout"


def test_retries_after_rate_limit():
    session = FakeSession([FakeResponse(429, text="rate limited"), FakeResponse(200, ROWS)])
    assert call(session) == ROWS
    assert len(session.calls) == 2


def test_retries_after_timeout():
    session = FakeSession([requests.Timeout("slow"), FakeResponse(200, ROWS)])
    assert call(session) == ROWS
    assert len(session.calls) == 2


def test_wrong_key_is_not_retried():
    session = FakeSession([FakeResponse(401, text="invalid token")])
    with pytest.raises(FetchError) as err:
        call(session)
    assert "401" in str(err.value)
    assert len(session.calls) == 1


def test_gives_up_after_max_retries():
    session = FakeSession([FakeResponse(503, text="down")] * 3)
    with pytest.raises(FetchError):
        call(session, max_retries=3)
    assert len(session.calls) == 3


def test_gives_up_after_repeated_connection_errors():
    session = FakeSession([requests.ConnectionError("no network")] * 3)
    with pytest.raises(FetchError):
        call(session, max_retries=3)
    assert len(session.calls) == 3


# ---------- parse_prices ----------

def test_parse_empty_list():
    df = parse_prices([], "SPY")
    assert list(df.columns) == PRICE_COLUMNS
    assert len(df) == 0


def test_parse_real_response():
    if not FIXTURE.exists():
        pytest.skip("Save a real API response to tests/fixtures/sample_response.json first (PLAN.md, Block 1)")
    rows = json.loads(FIXTURE.read_text())
    df = parse_prices(rows, "SPY")

    assert list(df.columns) == PRICE_COLUMNS
    assert len(df) == len(rows)
    assert (df["symbol"] == "SPY").all()
    assert df["date"].str.fullmatch(r"\d{4}-\d{2}-\d{2}").all(), "dates should look like 2024-01-02"
    assert df["date"].is_monotonic_increasing, "oldest first"
    for col in ["open", "high", "low", "close", "adj_close"]:
        assert pd.api.types.is_float_dtype(df[col]), f"{col} should be float"
    assert pd.api.types.is_integer_dtype(df["volume"])
    assert list(df.index) == list(range(len(df)))
