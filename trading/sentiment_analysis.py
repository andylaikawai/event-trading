import logging
from functools import reduce

from trading.sentiment_processor import execute_trade_based_on_sentiment
from model.news_event import NewsEvent
from trading.exchange import fetch_relevant_candles
from model.candles import Candles
from model.sentiment import Sentiment


def analyze_sentiment(news_event: NewsEvent):
    symbol = _process_suggestions(news_event)
    if not symbol:
        return

    timestamp = news_event.time
    
    previous_candle, observation_candles, performance_candles = fetch_relevant_candles(symbol, timestamp)
    if previous_candle is None or observation_candles is None or performance_candles is None:
        return

    sentiment = _get_sentiment(symbol, previous_candle, observation_candles)

    market_moved = execute_trade_based_on_sentiment(symbol, sentiment, observation_candles[-1], performance_candles)
    # if market_moved:
    #     source = news_event.link or news_event.url or "-"
    #     logging.info(f"{news_event.title}")
    #     logging.info(f"[ANALYSIS] Market moved by {market_moved:.2f}% at {news_event.datetime} for news: {source}")
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


def _get_sentiment(symbol: str, previous_candles: Candles, observation_candles: Candles) -> Sentiment:
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