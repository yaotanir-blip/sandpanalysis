# sandpanalysis: S&P 500 data pipeline and backtest

This project analyses S&P 500 data to investigate whether buying after a losing streak beats the buy-and-hold method, using a test period of 1478 trading days of data. 

## Origins

My IB project involved scraping S&P 500 prices into an Excel spreadsheet and analysing whether losing streaks are followed by a rebound. This project uses the same idea to compare this method with a buy-and-hold strategy. In addition, it now uses the Tiingo API instead of scraping, and includes data quality checks.

## What it does

1. **Fetches** daily SPY prices (an ETF that tracks the S&P 500) from the Tiingo API, with timeouts, retries and logging.
2. **Stores** them in SQLite, safely re-runnable, and queries them in SQL (`sql/queries.sql`).
3. **Checks** the data for ordering, duplicate, missing, non-positive, gap and outlier problems.
4. **Backtests** a streak strategy (buy after a run of down days, sell after a run of up days) with a stop-loss and trading costs.
5. **Tests it fairly:** thresholds come from 2014–2020 only, and the strategy is compared with buy-and-hold on 2021 onwards.

## Results

Test period: 4 Jan 2021 to 19 Nov 2026

| | Streak strategy | Buy and hold |
|---|---|---|
| Total return | +45.0% | +109.6% |
| Annualised return | 6.5% | 13.5% |
| Maximum drawdown | -13.0% | -24.5% |
| Number of trades | 219 | 1 |

![Equity curves on the test period](results/equity_test.png)

Generally, buy-and-hold resulted in a higher return, about twice that of the streak strategy. However, the largest difference is in the maximum drawdown, which is better for the strategy. A key consideration is the cost of making a larger number of trades, as the `COST_PER_TRADE` parameter is set to 0.001 (0.1%). Changing this cost to 0 raises the return to 80%, which is a significant difference. 

## Data checks

The data checks looked at whether the dates were in the right order, whether there were any duplicated rows, whether any cells for prices were missing, making sure prices were positive numbers, whether the daily change in the adjusted close was smaller than 20%, and making sure the rows had no more than a 5-day gap between trading days. 

## Assumptions

- Prices: adjusted close was used because it better reflects what real investors earned, by taking dividends and stock splits into account. 
- Trades happen at the close of the day the signal appears.
- Costs: 0.1% of the trade value on every buy and sell, as it is a reasonable cost charged to a retail investor.
- Stop-loss: 2% below the buy price.
- Limitations: only one ticker was used, and one test period was chosen. This model also doesn't take into account any taxes involved in trading. `run_fetch.py` also has to be run after the market closes to keep the rows complete. 

## Next steps

This model can be adjusted to analyse markets in several time intervals, and more trading methods can be compared alongside the buy-and-hold method already tested. 

## Run it yourself

```bash
python3 -m venv ~/.venvs/sandpanalysis
source ~/.venvs/sandpanalysis/bin/activate
pip install -r requirements.txt
cp .env.example .env        # add your free Tiingo API token
python run_fetch.py         # fetch, check and store prices
python run_backtest.py      # train/test backtest and chart
pytest                      # run the tests
```

## Project structure

The code lives in the `sandpa` package (short for sandpanalysis).

```
sandpa/
  config.py      settings: symbol, dates, costs, paths
  fetch.py       API requests, retries, parsing
  db.py          SQLite storage and queries
  clean.py       data quality checks
  strategy.py    returns, streaks, backtest, buy-and-hold
  metrics.py     total/annualised return, drawdown
run_fetch.py     pipeline: API → checks → database
run_backtest.py  train/test backtest and chart
tests/           tests for every module
```

## Data

Prices come from Tiingo's free plan, which is for internal use, so the raw data isn't included in this repository. Run `run_fetch.py` with your own token to download it.
