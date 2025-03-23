import json
import logging
from typing import List, Dict

from config import STARTING_CAPITAL
from type.news_event import NewsEvent
from type.type import Sentiment, Candle, Candles

MAX_NUMBER_OF_TRADES = 500

file_path = 'backtest/news_data.json'
current_capital = STARTING_CAPITAL
trades: List[Dict] = []


def load_historical_news():
    with open(file_path, 'r') as file:
        return json.load(file)


def run_backtest(news_data, on_historical_message):
    """Run backtesting using historical news data."""
    for news_event_data in news_data:
        if len(trades) >= MAX_NUMBER_OF_TRADES:
            logging.info(f"Reached the maximum number of trades: {MAX_NUMBER_OF_TRADES}")
            break
        news_event = NewsEvent.from_dict(news_event_data)
        message = json.dumps(news_event._asdict())
        on_historical_message(None, message)
    evaluate_results()


def paper_trade(symbol: str, sentiment: Sentiment, candles: Candles):
    if sentiment == Sentiment.NEUTRAL:
        logging.debug("[TRADE] Neutral sentiment detected. No trade executed.")
        return

    entry_price = candles[2].close
    entry_time = candles[2].timestamp
    trade_amount = current_capital / entry_price

    trade = {
        'symbol': symbol,
        'direction': sentiment.name,
        'amount': trade_amount,
        'entry_price': entry_price,
        'entry_time': entry_time,
        'exit_price': None,
        'exit_time': None,
        'price_change_percent': None,
        'pnl': None
    }
    trades.append(trade)
    logging.debug(f"[TRADE] Paper traded: {trade}")

    # Schedule exit after 30 minutes
    exit_trade(trade, candles)


def exit_trade(trade: Dict, candles: List[Candle], minutes: int = 29):
    global current_capital

    exit_time = trade['entry_time'] + 1000 * 60 * minutes
    exit_candle = next((candle for candle in candles if candle.timestamp >= exit_time), None)

    if exit_candle:
        trade['exit_price'] = exit_candle.close
        trade['exit_time'] = exit_candle.timestamp
        trade['price_change_percent'] = round(((trade['exit_price'] - trade['entry_price']) / trade['entry_price']) * 100, 2)
        trade['pnl'] = calculate_pnl(trade)
        current_capital += trade['pnl']
        logging.debug(f"[TRADE] Exited trade: {trade}")
        evaluate_results()


def calculate_pnl(trade: Dict) -> float:
    if trade['direction'] == Sentiment.POSITIVE.name:
        return (trade['exit_price'] - trade['entry_price']) * trade['amount']
    elif trade['direction'] == Sentiment.NEGATIVE.name:
        return (trade['entry_price'] - trade['exit_price']) * trade['amount']
    return 0.0


def evaluate_results():
    total_pnl = sum(trade['pnl'] for trade in trades if trade['pnl'] is not None)
    pnl_percentage = round((current_capital / STARTING_CAPITAL) * 100, 2)

    win_ratio = _get_win_ratio()

    logging.info(f"[Trade] Total trades made: {len(trades)}")
    logging.info(f"[Trade] Total PnL: {total_pnl}")
    logging.info(f"[Trade] Win Ratio: {win_ratio}")
    logging.info(f"[Trade] Performance: {pnl_percentage}%")

def _get_win_ratio() -> float:
    if not trades:
        return 0.0
    winning_trades = sum(1 for trade in trades if trade['pnl'] > 0)
    return winning_trades / len(trades) * 100