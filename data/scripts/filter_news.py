from config import RAW_FILTERED_NEWS_FILE, FROM_DATE, TO_DATE
from data.scripts.fetch_all_news import get_all_news
from utils.util import format_time, parse_datetime_to_timestamp, read_from_cache_or_fetch

from_timestamp = parse_datetime_to_timestamp(FROM_DATE)
to_timestamp = parse_datetime_to_timestamp(TO_DATE)


def _filter_raw_news_by_date_range():
    raw_news = get_all_news()

    print(f"Total number of raw news events: {len(raw_news)}")
    print(f"Latest news: {format_time(raw_news[0].get('time'), '%Y%m%d %H:%M:%S')}")
    print(f"Oldest news: {format_time(raw_news[-1].get('time'), '%Y%m%d %H:%M:%S')}")
    print(f"Filtering news from {FROM_DATE} to {TO_DATE}")

    filtered_news = list(filter(lambda x: to_timestamp > x.get('time') >= from_timestamp, raw_news))

    print(f"Filtered news count: {len(filtered_news)}")

    return filtered_news

def get_filtered_news():
    return read_from_cache_or_fetch(RAW_FILTERED_NEWS_FILE, _filter_raw_news_by_date_range)