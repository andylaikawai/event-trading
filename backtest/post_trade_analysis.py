import logging
from typing import Union

from model.candles import Candles
from model.news_event import HistoricalNewsEvent


def post_trade_analysis(news_event: HistoricalNewsEvent) -> None:
    # TODO identify missed opportunities
    market_moved = _detect_price_movement(news_event.performance_candles)

    if market_moved:
        source = news_event.url or "-"
        logging.debug(f"{news_event.title}")
        logging.debug(f"[ANALYSIS] Market moved by {market_moved:.2f}% at {news_event.datetime} for news: {source}")


def _detect_price_movement(candles: Candles) -> Union[float, None]:
    """Detect if the market price moved by more than 2%."""
    if candles is None or len(candles) < 2:
        return None

    initial_price = candles[0].close
    final_price = candles[-1].close

    price_change = (final_price - initial_price) / initial_price

    abs_price_change = abs(price_change)
    if abs_price_change > 0.02:
        return price_change * 100

    return None
