import logging
from functools import reduce
from typing import Tuple, Optional

from trading.sentiment_processor import execute_trade_based_on_sentiment
from type.news_event import NewsEvent
from config import MAX_OBSERVATION_PERIOD, MAX_HOLDING_PERIOD, LOOK_BACK_PERIOD
from trading.exchange import exchange
from type.type import Candles, Candle, Sentiment
from utils.util import min_to_ms

def analyze_sentiment(news_event: NewsEvent):
    symbol = _process_suggestions(news_event)
    if not symbol:
        return

    timestamp = news_event.time
    
    previous_candle, observation_candles, performance_candles = _fetch_market_price(symbol, timestamp)
    if previous_candle is None or observation_candles is None or performance_candles is None:
        return

    sentiment = _get_sentiment(symbol, previous_candle, observation_candles)

    market_moved = execute_trade_based_on_sentiment(symbol, sentiment, observation_candles[-1], performance_candles)
    if market_moved:
        source = news_event.link or news_event.url or "-"
        logging.info(f"{news_event.title}")
        logging.info(f"[ANALYSIS] Market moved by {market_moved:.2f}% at {news_event.datetime} for news: {source}")
    return

def _process_suggestions(news_event: NewsEvent):
    suggestions = news_event.suggestions
    if suggestions:
        for suggestion in suggestions:
            coin = suggestion.get("coin")
            if coin:
                logging.debug(f"Relevant coin identified: {coin}")
                return coin
    else:
        return None

def _fetch_market_price(symbol: str, timestamp: int) -> Tuple[Optional[Candles], Optional[Candles], Optional[Candles]]:
    number_of_candles = LOOK_BACK_PERIOD + MAX_OBSERVATION_PERIOD + MAX_HOLDING_PERIOD
    start_candle_timestamp = timestamp - min_to_ms(LOOK_BACK_PERIOD)

    try:
        ohlcv = exchange.fetch_ohlcv(f"{symbol}/USDT", timeframe='1m', since=start_candle_timestamp, limit=number_of_candles)
        candles = [Candle.from_ohlcv(candle) for candle in ohlcv]

        # Split candles into previous/current for sentiment analysis and future for performance evaluation
        # TODO this is backtest specific
        observe_until = timestamp + min_to_ms(MAX_OBSERVATION_PERIOD)
        previous_candles = [candle for candle in candles if candle.timestamp <= timestamp]
        observation_candles = [candle for candle in candles if timestamp < candle.timestamp <= observe_until]
        performance_candles = [candle for candle in candles if candle.timestamp > observe_until]

        return previous_candles, observation_candles, performance_candles

    except Exception as e:
        logging.debug(f"[ERROR] Failed to fetch market price: {e}")
        return None, None, None

def _get_sentiment(symbol: str, previous_candles: Candles, observation_candles: Candles) -> Sentiment:
    if previous_candles is None or observation_candles is None:
        return Sentiment.NEUTRAL

    first_candle = previous_candles[0]
    current_candle = observation_candles[-1]
    previous_close = first_candle.close
    previous_volume_avg = _get_average_volume(previous_candles)

    current_close = current_candle.close
    observed_volume_avg = _get_average_volume(observation_candles)

    volume_spiked = observed_volume_avg >= previous_volume_avg * 10 # TODO parametized

    if volume_spiked:
        if current_close > previous_close * 1.001:
            logging.debug(f"[TRADE] Positive sentiment detected for {symbol}.")
            return Sentiment.POSITIVE
        elif current_close < previous_close * 0.999:
            logging.debug(f"[TRADE] Negative sentiment detected for {symbol}.")
            return Sentiment.NEGATIVE
    return Sentiment.NEUTRAL

def _get_average_volume(candles: Candles):
    return reduce(lambda x, y: x + y, map(lambda candle: candle.volume, candles)) / len(candles)



# def analyze_sentiment(news_event):
#
#     prompt = f"""
#     Determine sentiment (Positive, Negative, Neutral) for the following crypto news. Respond with ONE word only.
#
#     Headline: {headline}
#     Content: {content}
#     Sentiment:
#     """
#     # To implement: Call to OpenAI or another sentiment analysis API
#     return "Neutral"  # Placeholder return value