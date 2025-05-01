import logging
from functools import reduce

from backtest.sentiment_processor import execute_trade_based_on_sentiment
from data.scripts.data_config import COIN
from model.candles import Candles
from model.news_event import NewsEvent, HistoricalNewsEvent
from model.sentiment import Sentiment


def analyze_sentiment(news_event: HistoricalNewsEvent):
    sentiment = _get_sentiment(COIN, news_event.previous_candles, news_event.observation_candles)

    # FIXME it is unfair to analyse future data and trade at an older timestamp, this is for illustration purpose only
    execution_candle = news_event.observation_candles[0]
    # execution_candle = news_event.observation_candles[-1]

    # FIXME below also support multiple performance candles to trigger take profit/stop loss
    market_moved = execute_trade_based_on_sentiment(COIN, sentiment, execution_candle, [news_event.performance_candle])

    # TODO identify missed opportunities
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

    # TODO toy example below to detect volume spike / price movement.
    volume_spiked = observed_volume_avg >= previous_volume_avg * 3

    if volume_spiked:
        if current_close > previous_close * 1.002:
            logging.debug(f"[TRADE] Positive sentiment detected for {symbol}.")
            return Sentiment.POSITIVE
        elif current_close < previous_close * 0.998:
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