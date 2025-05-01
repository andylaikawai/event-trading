import requests

from data.scripts.data_config import TREE_ALL_NEWS_API
from utils.util import read_from_cache_or_fetch

OUTPUT_FILE = "data/raw_all_news.json"

def _fetch_all_news():
    try:
        print(f"Fetching news data from {TREE_ALL_NEWS_API}...")
        response = requests.get(TREE_ALL_NEWS_API)
        response.raise_for_status()  # Raise an error for HTTP issues
        news_data = response.json()
        print(f"Successfully fetched {len(news_data)} number of news events")
        return news_data

    except requests.RequestException as e:
        print(f"Failed to fetch news data: {e}")

def get_all_news():
    return read_from_cache_or_fetch(OUTPUT_FILE, _fetch_all_news)