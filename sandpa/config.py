"""Project settings. Change values here rather than inside the code."""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "results"
DB_PATH = DATA_DIR / "prices.db"

# What to analyse
SYMBOL = "SPY"            # ETF that tracks the S&P 500 (index data itself usually isn't on free APIs)
START_DATE = "2014-01-01"
TRAIN_END = "2020-12-31"  # thresholds are worked out on data up to here, then tested on data after it

# Backtest assumptions: pick your own values and justify them in the README
COST_PER_TRADE = 0.001    # fraction of the trade value paid on every buy and every sell (0.001 = 0.1%)
STOP_LOSS = 0.02          # sell if the close falls 2% or more below the buy price
START_CASH = 1000.0

# Data source
API_BASE_URL = "https://api.tiingo.com/tiingo/daily"


def get_api_key() -> str:
    """Read the Tiingo API key from the environment (or from a .env file in the project folder)."""
    try:
        from dotenv import load_dotenv
        load_dotenv(PROJECT_ROOT / ".env")
    except ImportError:
        pass  # python-dotenv not installed: the key must already be in the environment

    key = os.environ.get("TIINGO_API_KEY")
    if not key:
        raise RuntimeError(
            "TIINGO_API_KEY is not set. Copy .env.example to .env and put your key in it (see README)."
        )
    return key
