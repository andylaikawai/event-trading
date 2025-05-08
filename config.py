import logging

# Logging Configuration
LOG_LEVEL = logging.INFO
DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Data Source
TREE_ALL_NEWS_API = "https://news.treeofalpha.com/api/allNews"
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
TAKE_PROFIT = 0.25
STOP_LOSS = -0.01


# Backtesting Configuration
IS_BACKTEST_MODE = True  # Set this to True to enable backtesting
FROM_DATE = '20250301'
TO_DATE = '20250401'
SYMBOL = 'BTC'
NUMBER_OF_PREVIOUS_CANDLES = 10
NUMBER_OF_OBSERVATION_CANDLES = 10
NUMBER_OF_PERFORMANCE_CANDLES = 60
# Cache Location
RAW_ALL_NEWS_FILE = 'data/raw_all_news.json'
RAW_FILTERED_NEWS_FILE = f'data/raw_news_{FROM_DATE}_{TO_DATE}.json'
RAW_CANDLES_FILE = f'data/raw_candles_{FROM_DATE}_{TO_DATE}_{SYMBOL}.json'
PROCESSED_DATA_OUTPUT_FILE = f'data/preprocessed_news_{FROM_DATE}_{TO_DATE}_{SYMBOL}.json'