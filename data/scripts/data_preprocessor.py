import json
from typing import Optional, Tuple

from config import MAX_OBSERVATION_PERIOD, MAX_HOLDING_PERIOD
from data.scripts.data_config import FROM_DATE, TO_DATE, COIN, PROCESSED_DATA_OUTPUT_FILE
from data.scripts.fetch_candles import get_candles
from data.scripts.filter_news import get_filtered_news
from model.candles import Candles
from model.news_event import NewsEvent, HistoricalNewsEvent
from utils.util import parse_datetime_to_timestamp, min_to_ms, read_from_cache_or_fetch


def preprocess_news_data():
    raw_news = get_filtered_news()

    # Get all candles within time range
    from_timestamp = parse_datetime_to_timestamp(FROM_DATE)
    to_timestamp = parse_datetime_to_timestamp(TO_DATE)
    all_candles = get_candles(from_timestamp, to_timestamp)

    # Project specified keys, filter by coin, and populate relevant candles
    processed_news = []
    for news in raw_news:
        if any(suggestion.get("coin") == COIN for suggestion in news.get("suggestions", [])):
            timestamp = news.get("time")
            previous_candles, observation_candles, performance_candles = _get_relevant_candles(all_candles, timestamp)

            # TODO maybe model the data specifically for challenge purpose
            processed_news.append({
                "title": news.get("title"),
                "time": news.get("time"),
                "url": news.get("url"),
                "source": news.get("source"),
                "previous_candles": previous_candles,
                "observation_candles": observation_candles,
                "performance_candle": performance_candles[-1]
            })

    print(f"Processed news count: {len(processed_news)}")

    return processed_news

def get_preprocessed_news():
    return read_from_cache_or_fetch(PROCESSED_DATA_OUTPUT_FILE, preprocess_news_data, indent=4)



def _get_relevant_candles(candles: Candles, timestamp: int) -> Tuple[Optional[Candles], Optional[Candles], Optional[Candles]]:
    observe_since = timestamp - min_to_ms(MAX_OBSERVATION_PERIOD)
    observe_until = timestamp + min_to_ms(MAX_OBSERVATION_PERIOD)
    hold_until = timestamp + min_to_ms(MAX_HOLDING_PERIOD)

    previous_candles = [candle for candle in candles if observe_since <= candle.timestamp < timestamp]
    observation_candles = [candle for candle in candles if timestamp <= candle.timestamp <= observe_until]
    performance_candles = [candle for candle in candles if timestamp <= candle.timestamp <= hold_until]
    return previous_candles, observation_candles, performance_candles

if __name__ == "__main__":
    get_preprocessed_news()
