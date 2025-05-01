# Tech Stack
- Python 3.9.6

# How to use

1. run `raw_data/fetch_all_news.bash` to download the raw news data from TreeNews (~300MB). Output `all_news.json`
2. run `raw_data/filter_news.py` to filter the raw news data with a smaller timeframe. Output `raw_news_[from_date]_[to_date].json`
3. run `main.py` to start backtesting. See `config.py` for configuration. Output `.logs` files.