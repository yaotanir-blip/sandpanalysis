# sandpanalysis: one-week plan (rebuilding Dionysus)

Goal: by the end of the week, a working project on GitHub you can put on your CV and defend line by line. It should give you real evidence for: Python + pandas + SQL, working with an API (including handling failures), data quality checks, and a fair backtest.

## How we work

- **You write the code** in `sandpa/` and the two `run_*.py` scripts. Each function has a docstring saying exactly what it must do.
- **The tests are the spec.** Each block is done when its tests pass. Don't change a test to make it pass; if you think a test is wrong, ask.
- **One block at a time, with Claude.** Before each block, ask for a short explanation of the ideas. When you're stuck or done, paste your code for review. Expect hints, not finished code.
- **Commit after every block** with a message that says what you did.
- **Be honest about AI use.** If an interviewer asks, say plainly what you wrote and how you used AI. A clear answer goes down far better than a vague one.

## Day 0: setup (30 min)

1. Make a free account at tiingo.com and copy your API token (Account → API → Token).
   Free plan: 50 requests an hour, 1,000 a day, internal use only. That's plenty: 10 years of SPY is one request.
2. In Terminal:
   ```bash
   cd "$HOME/Library/CloudStorage/OneDrive-UniversityCollegeLondon/Claude code/sandpanalysis"
   python3 -m venv ~/.venvs/sandpanalysis      # outside OneDrive, so it doesn't sync thousands of files
   source ~/.venvs/sandpanalysis/bin/activate
   pip install -r requirements.txt
   cp .env.example .env                   # then paste your token into .env
   pytest
   ```
3. Expect lots of failures saying `NotImplementedError`, and one skipped test. That's your to-do list.
4. `git init`, first commit, and create an empty GitHub repo (e.g. `yaotanir-blip/sandpanalysis`).

## Block 1: fetch (Day 1) → `sandpa/fetch.py`

1. **Explore first.** In a Python shell, make one request by hand for SPY over one month. Check Tiingo's docs ("Connecting" and "End-of-Day") for how to send your token. Print the status code, the number of rows and the first row. Save that response to `tests/fixtures/sample_response.json`.
2. Write `parse_prices`. Check: `pytest tests/test_fetch.py -k parse -v`
3. Write `fetch_prices` with timeouts, retries and logging. Check: `pytest tests/test_fetch.py -v`

Learn: HTTP status codes (200, 401, 404, 429, 5xx), JSON, timeouts, retrying with exponential backoff, why keys live in `.env`.
Be able to answer: *What does a 429 mean and what should a client do? Why always set a timeout? What does your code do if the network drops?*

## Block 2: store (Day 2) → `sandpa/db.py`, `run_fetch.py`

1. `create_table`, 2. `save_prices`, 3. `load_prices`. Check: `pytest tests/test_db.py -v`
4. Write `run_fetch.py` and run it **twice**. The second run should insert 0 rows.
5. **SQL practice.** Open the database (`sqlite3 data/prices.db`) and write three queries yourself. Save them in `sql/queries.sql`:
   - number of trading days per year (`GROUP BY` on the year)
   - the 5 biggest one-day falls (look up `LAG()`)
   - average daily range (high − low) per year

Learn: primary keys, why a pipeline should be safe to re-run, parameterised queries vs SQL injection.
Be able to answer: *What happens if you run the pipeline twice? What is SQL injection and how did you avoid it?*

## Block 3: check the data (Day 3) → `sandpa/clean.py`

1. `find_problems`, 2. `clean_prices`. Check: `pytest tests/test_clean.py -v`
3. Run the checks on the real data and write down what they found, even if nothing.
4. Optional, but a good interview story: load your old `Year 1 From August 2nd 2024.xlsx` (needs `pip install openpyxl`) and show `find_problems` catches the day/month swap.

Be able to answer: *How do you know your data is right? Tell me about a data problem you found and fixed.*

## Block 4: the strategy (Day 4) → `sandpa/strategy.py`

1. Work through the examples in `tests/test_strategy.py` **on paper first**. If you can't get the expected numbers by hand, the code won't either.
2. `daily_returns`, `streak_lengths`, `average_streaks`, then `backtest_streaks`, then `buy_and_hold`. Check: `pytest tests/test_strategy.py -v`

Note `test_stop_loss_losses_are_counted`: it's the bug from your 2024 script.
Be able to answer: *Walk me through your backtest rules. What do you assume about when trades happen? Why include costs?*

## Block 5: a fair test (Day 5) → `sandpa/metrics.py`, `run_backtest.py`

1. Metrics. Check: `pytest tests/test_metrics.py -v`
2. `run_backtest.py`: thresholds from 2014–2020 only, tested on 2021 onwards, against buy-and-hold, with a chart.
3. Whatever the result, it's fine. "The strategy lost to buy-and-hold, and here's why" is a perfectly good finding.

Learn: look-ahead bias, overfitting, in-sample vs out-of-sample, drawdown.
Be able to answer: *Did it beat buy-and-hold? Why or why not? How did you avoid fooling yourself?*

## Block 6: write-up and publish (Day 6)

1. Fill in every `[placeholder]` in `README.md` in your own words: results table, chart, data checks, limitations, next steps.
2. Make sure `.env` and `data/` are **not** in the repo (`git status`), then push to GitHub.
3. Draft the CV bullet using your real numbers, then check it with Claude.

## Day 7: buffer

Catch up, tidy the code, re-read your answers to the "Be able to answer" questions.

## After the week (optional)

- **For Bloomberg:** send FIX messages between two local Python programs over TCP (`simplefix` + `socket`). Covers the FIX and TCP/IP line.
- **For data science and ML roles:** a simple scikit-learn model predicting next-day direction, compared with always guessing "up". Expect it to be close to random; saying so honestly is the point.
- More tickers (e.g. a few ETFs) to see whether the result holds outside SPY.
