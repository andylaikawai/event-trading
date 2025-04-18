import logging

from trading.sentiment_processor import execute_trade_based_on_signals
from type.news_event import NewsEvent


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

def analyze_sentiment(news_event: NewsEvent):
    symbol = _process_suggestions(news_event)
    timestamp = news_event.time

    if symbol == "BTC":
        market_moved = execute_trade_based_on_signals(symbol, timestamp)
        if market_moved:
            source = news_event.link or news_event.url or "-"
            logging.info(f"{news_event.title}")
            logging.info(f"[ANALYSIS] Market moved by {market_moved:.2f}% at {news_event.datetime} for news: {source}")
    return


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