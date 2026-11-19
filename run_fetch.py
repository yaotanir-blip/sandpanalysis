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
    # 1. Fetch
    rows = fetch_prices(config.SYMBOL,config.START_DATE,)                 # config.SYMBOL and config.START_DATE
    log.info("Fetched %d rows", len(rows))

    # 2. Parse
    df = parse_prices(rows,config.SYMBOL)                                 # the same call as in your Python shell test

    # 3. Data checks: added in Block 3

    # 4. Database
    config.DATA_DIR.mkdir(exist_ok=True)     # creates data/ if missing; fine if it already exists
    conn = connect(config.DB_PATH)
    create_table(conn)

    # 5. Save
    inserted = save_prices(conn,df)                           # save_prices returns the number of new rows
    log.info("Inserted %d new rows into %s", inserted, config.DB_PATH)
    conn.close()


if __name__ == "__main__":
    main()
