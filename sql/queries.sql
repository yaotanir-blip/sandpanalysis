.headers on
.mode column
                                           
SELECT strftime('%Y', date) AS year, COUNT(*) AS trading_days 
FROM prices     
GROUP BY year
ORDER BY year;

SELECT strftime('%Y', date) AS year FROM prices LIMIT 5;           
SELECT strftime('%Y', date) AS year, ROUND(AVG((high-low)/close * 100),2) AS avg_range_pct
FROM prices     
GROUP BY year
ORDER BY year;

WITH daily AS (
    SELECT date,
           adj_close,
           LAG(adj_close) OVER (ORDER BY date) AS prev_close
    FROM prices
    WHERE symbol = 'SPY'
)
SELECT date, ROUND(((adj_close-prev_close)*100/prev_close),2) AS change_pct             -- the % change, using adj_close and prev_close
FROM daily
WHERE prev_close IS NOT NULL                      -- the first day has no previous close
ORDER BY change_pct                   -- biggest falls first
