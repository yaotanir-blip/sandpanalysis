"""Block 5, step 2: a fair test of the streak strategy against buy-and-hold.

Run from the project folder:  python run_backtest.py
"""
import pandas as pd
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
    # 1. Load and clean; keep just the adjusted close, indexed by date
    conn = connect(config.DB_PATH)
    df = clean_prices(load_prices(conn, config.SYMBOL))
    conn.close()
    prices = df.set_index("date")["adj_close"]

    # 2. Split into train and test
    train = prices[prices.index <= config.TRAIN_END]
    test = prices[prices.index > config.TRAIN_END]                                   # everything after TRAIN_END
    log.info("Train: %d days, test: %d days", len(train), len(test))

    # 3. Thresholds from the TRAINING data only
    avg_up, avg_down = average_streaks(daily_returns(train))
    log.info("Average up run %.2f days, down run %.2f days", avg_up, avg_down)

    # 4. Run both on the TEST data
    equity, trades = backtest_streaks(
        test,
        buy_after=avg_down,                           # which average? You buy after a LOSING run
        sell_after=avg_up,                          # and sell after a winning one
        stop_loss=config.STOP_LOSS,
        cost=config.COST_PER_TRADE,
        start_cash=config.START_CASH,
    )
    bench = buy_and_hold(test, cost=config.COST_PER_TRADE, start_cash=config.START_CASH)

    # 5. Compare side by side
    results = pd.DataFrame({"Streak strategy": summary(equity, trades),
                            "Buy and hold": summary(bench)})
    print(results.round(3))

    # 6. Chart
    config.RESULTS_DIR.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(equity.index, equity, label="Streak strategy")
    ax.plot(bench.index, bench, label="Buy and hold")
    ax.set_title(f"{config.SYMBOL}: Streak strategy vs buy and hold, {test.index[0].date()} to {test.index[-1].date()}")                            # e.g. what, which ticker, which period
    ax.set_ylabel("Value ($)")                           # SPY trades in dollars
    ax.legend()
    fig.savefig(config.RESULTS_DIR / "equity_test.png", dpi=150, bbox_inches="tight")
    log.info("Chart saved to %s", config.RESULTS_DIR / "equity_test.png")


if __name__ == "__main__":
    main()
