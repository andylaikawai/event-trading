import logging

from backtest.sentiment_analysis import analyze_sentiment
from logger import display_news
from model.news_event import HistoricalNewsEvent


def on_historical_news_event(news_event: HistoricalNewsEvent):
    try:
        display_news(news_event)
        analyze_sentiment(news_event)

    except Exception as e:
        logging.error(f"[ERROR] Processing Error: {e}")