"""Block 5, step 2: a fair test of the streak strategy against buy-and-hold.

Run from the project folder:  python run_backtest.py
"""

import logging

import matplotlib.pyplot as plt

from sandpa import config
from sandpa.clean import clean_prices
from sandpa.db import connect, load_prices
from sandpa.metrics import summary
from sandpa.strategy import average_streaks, backtest_streaks, buy_and_hold, daily_returns

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("run_backtest")


def main():
    # TODO:
    # 1. Load the stored prices for config.SYMBOL and clean them. Use adj_close as the price
    #    series (index = date). Why adjusted and not close? Write the answer in the README.
    # 2. Split into train (up to config.TRAIN_END) and test (after it).
    # 3. Work out the average up and down streaks on TRAIN ONLY. These are your thresholds.
    #    (The 2024 version used the whole dataset here: that's look-ahead bias.)
    # 4. On TEST: run backtest_streaks (with config.STOP_LOSS and config.COST_PER_TRADE)
    #    and buy_and_hold (same cost).
    # 5. Print both summaries side by side.
    # 6. Plot both equity curves on one chart and save it to config.RESULTS_DIR / "equity_test.png".
    raise NotImplementedError


if __name__ == "__main__":
    main()
