"""Block 2, step 4: fetch prices from the API, check them, and store them.

Run from the project folder:  python run_fetch.py
Running it twice should not create duplicate rows.
"""

import logging

from sandpa import config
from sandpa.clean import find_problems
from sandpa.db import connect, create_table, save_prices
from sandpa.fetch import fetch_prices, parse_prices

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("run_fetch")


def main():
    # TODO:
    # 1. Fetch the raw rows for config.SYMBOL from config.START_DATE.
    # 2. Parse them into a DataFrame.
    # 3. Run find_problems on it and log each problem as a warning (don't stop: look at them).
    # 4. Make sure config.DATA_DIR exists, connect to config.DB_PATH and create the table.
    # 5. Save the prices and log how many new rows were inserted.
    raise NotImplementedError


if __name__ == "__main__":
    main()
