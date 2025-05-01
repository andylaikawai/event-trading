# data source
TREE_ALL_NEWS_API = "https://news.treeofalpha.com/api/allNews"

# input
FROM_DATE = '20250301'
TO_DATE = '20250401'
COIN = 'BTC'

# output
RAW_ALL_NEWS_FILE = 'data/raw_all_news.json'
RAW_FILTERED_NEWS_FILE = f'data/raw_news_{FROM_DATE}_{TO_DATE}.json'
RAW_CANDLES_FILE = f'data/raw_candles_{FROM_DATE}_{TO_DATE}_{COIN}.json'
PROCESSED_DATA_OUTPUT_FILE = f'data/preprocessed_news_{FROM_DATE}_{TO_DATE}_{COIN}.json'