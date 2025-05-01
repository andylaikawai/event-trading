import json
from typing import Optional, Tuple

from config import MAX_OBSERVATION_PERIOD, MAX_HOLDING_PERIOD
from model.candles import Candles, Candle
from trading.exchange import fetch_candles_from_exchange
from utils.util import format_time, parse_datetime_to_timestamp, min_to_ms

# input
FROM_DATE = '20250301'
TO_DATE = '20250401'
COIN = 'BTC'
RAW_DATA_INPUT_FILE = f'../../raw_data/raw_news_{FROM_DATE}_{TO_DATE}.json'

# output
CACHED_CANDLES_FILE = f'candles_{FROM_DATE}_{TO_DATE}_{COIN}.json'
PROCESSED_DATA_OUTPUT_FILE = f'preprocessed_news_{FROM_DATE}_{TO_DATE}_{COIN}.json'

def preprocess_news_data(input_file: str, output_file: str):
    with open(input_file, 'r') as file:
        raw_news = json.load(file)

    # Get all candles within time range
    from_timestamp = parse_datetime_to_timestamp(FROM_DATE)
    to_timestamp = parse_datetime_to_timestamp(TO_DATE)
    all_candles = _fetch_candles(from_timestamp, to_timestamp)

    # Project specified keys, filter by coin, and populate relevant candles
    processed_news = []
    for news in raw_news:
        if any(suggestion.get("coin") == COIN for suggestion in news.get("suggestions", [])):
            timestamp = news.get("time")
            previous_candles, observation_candles, performance_candles = _get_relevant_candles(all_candles, timestamp)
            processed_news.append({
                "title": news.get("title"),
                "time": news.get("time"),
                "url": news.get("url"),
                "source": news.get("source"),
                "previous_candles": previous_candles,
                "observation_candles": observation_candles,
                "performance_candles": performance_candles,
            })

    print(f"Processed news count: {len(processed_news)}")

    with open(output_file, 'w') as file:
        json.dump(processed_news, file)

def _fetch_candles(from_timestamp: int, to_timestamp: int) -> Optional[Candles]:
    try:
        with open(CACHED_CANDLES_FILE, 'r') as cache_file:
            cached_candles = json.load(cache_file)
            return [Candle.from_ohlcv(candle) for candle in cached_candles]
    except FileNotFoundError:
        ohlcv = fetch_candles_from_exchange(symbol=f"{COIN}/USDT", from_timestamp=from_timestamp, to_timestamp=to_timestamp)
        if not ohlcv:
            raise ValueError(f"Failed to fetch market price for coin: {COIN} from {format_time(from_timestamp)} to {format_time(to_timestamp)}")
        candles = [Candle.from_ohlcv(candle) for candle in ohlcv]
        with open(CACHED_CANDLES_FILE, 'w') as cache_file:
            json.dump(candles, cache_file)
        return candles

def _get_relevant_candles(candles: Candles, timestamp: int) -> Tuple[Optional[Candles], Optional[Candles], Optional[Candles]]:
    observe_since = timestamp - min_to_ms(MAX_OBSERVATION_PERIOD)
    observe_until = timestamp + min_to_ms(MAX_OBSERVATION_PERIOD)
    hold_until = timestamp + min_to_ms(MAX_HOLDING_PERIOD)

    previous_candles = [candle for candle in candles if observe_since <= candle.timestamp < timestamp]
    observation_candles = [candle for candle in candles if timestamp <= candle.timestamp <= observe_until]
    performance_candles = [candle for candle in candles if timestamp <= candle.timestamp <= hold_until]
    return previous_candles, observation_candles, performance_candles

if __name__ == "__main__":
    preprocess_news_data(RAW_DATA_INPUT_FILE, PROCESSED_DATA_OUTPUT_FILE)
    print(f"Processed news data saved to {PROCESSED_DATA_OUTPUT_FILE}")