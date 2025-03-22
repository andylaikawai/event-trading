import json
import logging
import time

from type.type import Sentiment

file_path = 'backtest/news_data.json'

def load_historical_news():
    with open(file_path, 'r') as file:
        return json.load(file)

def run_backtest(news_data, on_historical_message):
    """Run backtesting using historical news data."""
    for news_event in news_data:
        message = json.dumps(news_event)
        on_historical_message(None, message)
    evaluate_results()

trades = []  # Store trades made during backtesting

def paper_trade(symbol: str, trade_amount: float, sentiment: Sentiment):
    if sentiment == Sentiment.NEUTRAL:
        logging.info("[TRADE] Neutral sentiment detected. No trade executed.")
        return

    trade = {
        'symbol': symbol,
        'direction': sentiment.name,
        'amount': trade_amount,
        'timestamp': time.time()
    }
    trades.append(trade)
    logging.info(f"[TRADE] Paper traded: {trade}")

def evaluate_results():
    print(f"[Trade] Total trades made: {len(trades)}")
