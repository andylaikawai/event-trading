import logging

# Logging Configuration
LOG_LEVEL = logging.INFO
DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Tree News Configuration
TREE_NEWS_API_KEY = 'b16f4e167abb76fb574622e7428d87e8a0f98443fa8019281ad239eb95f56758'
WS_URLS = [
    "wss://news.treeofalpha.com/ws",
    "ws://tokyo.treeofalpha.com:5124/ws"
]

# BINANCE API Configuration
BINANCE_API_KEY = 'YOUR_BINANCE_API_KEY'
BINANCE_SECRET = 'YOUR_BINANCE_SECRET'
BINANCE_PASSPHRASE = 'YOUR_BINANCE_API_PASSPHRASE'


# Trading Bot Configuration
STARTING_CAPITAL = 1000
MAX_HOLDING_PERIOD = 30  # minutes
MAX_OBSERVATION_PERIOD = 3 # minutes
LOOK_BACK_PERIOD = 3 # minutes
TAKE_PROFIT = 0.05
STOP_LOSS = -0.01


# Backtesting Configuration
IS_BACKTEST_MODE = True  # Set this to True to enable backtesting
RAW_NEWS_FILE = 'data/raw_news_20250301_20250401.json'