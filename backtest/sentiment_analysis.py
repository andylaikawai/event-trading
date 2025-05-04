import logging
from functools import reduce

from model.candles import Candles
from model.news_event import NewsEvent, HistoricalNewsEvent
from model.sentiment import Sentiment
from model.trade_params import TradeParams


def analyze_sentiment(params: TradeParams, news_event: HistoricalNewsEvent, symbol: str) -> Sentiment:
    return _get_sentiment(params, symbol, news_event.previous_candles, news_event.observation_candles)


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


def _get_sentiment(params: TradeParams, symbol: str, previous_candles: Candles, observation_candles: Candles) -> Sentiment:
    if len(previous_candles) < params.look_back_period:
        raise ValueError(f"Not enough previous candles ({len(previous_candles)}). LOOKBACK_PERIOD is set to {params.look_back_period} minutes. Refresh raw candle data")
    if len(observation_candles) < params.max_observation_period:
        raise ValueError(f"Not enough observation candles ({len(previous_candles)}). MAX_OBSERVATION_PERIOD is set to {params.look_back_period} minutes. Refresh raw candle data")

    previous_candles = previous_candles[-params.look_back_period:]
    observation_candles = observation_candles[:params.max_observation_period]

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
