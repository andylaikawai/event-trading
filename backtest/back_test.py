import json
import logging
from typing import List, Dict

from config import STARTING_CAPITAL, TAKE_PROFIT, STOP_LOSS, RAW_NEWS_FILE
from model.news_event import NewsEvent
from model.candles import Candle, Candles
from model.sentiment import Sentiment
from utils.util import round_to_2dp

MAX_NUMBER_OF_TRADES = 500


current_capital = STARTING_CAPITAL
trades: List[Dict] = []


def load_historical_news() -> [Dict]:
    with open(RAW_NEWS_FILE, 'r') as file:
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
    _evaluate_result()


def paper_trade(symbol: str, sentiment: Sentiment, candle: Candle, performance_candles: Candles):
    if sentiment == Sentiment.NEUTRAL:
        logging.debug("[TRADE] Neutral sentiment detected. No trade executed.")
        return
    if any(trade['symbol'] == symbol and trade['entry_time'] == candle.timestamp for trade in trades):
        logging.debug(f"[TRADE] Duplicate trade detected for {symbol} at {candle.timestamp}. Skipping trade.")
        return

    entry_price = candle.close
    entry_time = candle.timestamp
    trade_amount = current_capital / entry_price

    [f_amount] = round_to_2dp(trade_amount)
    trade = {
        'symbol': symbol,
        'direction': sentiment.name,
        'amount': f_amount,
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
    _exit_trade(trade, performance_candles)

def _get_exit_candle(trade: Dict, candles: Candles, exit_time: int) -> Candle:
    entry_price = trade['entry_price']
    direction = trade['direction']

    for candle in candles:
        if candle.timestamp >= exit_time:
            logging.info(f"[TRADE] Exit time")
            return candle

        gain = (candle.close - entry_price) / entry_price
        if direction == Sentiment.NEGATIVE.name:
            gain *= -1
        if gain >= TAKE_PROFIT:
            logging.info(f"[TRADE] Take profit")
            return candle
        if gain <= STOP_LOSS:
            logging.info(f"[TRADE] Stop loss")
            return candle

    return candles[-1]

def _exit_trade(trade: Dict, candles: Candles, minutes: int = 29):
    global current_capital

    exit_time = trade['entry_time'] + 1000 * 60 * minutes
    entry_price = trade['entry_price']
    exit_candle = _get_exit_candle(trade, candles, exit_time)

    exit_price = exit_candle.close
    price_change_percent = ((exit_price - entry_price) / entry_price) * 100
    trade['exit_price'] = exit_price
    trade['exit_time'] = exit_candle.timestamp
    trade['price_change_percent'] = round_to_2dp(price_change_percent)[0]
    trade['pnl'] = round_to_2dp(_calculate_pnl(trade))[0]
    current_capital += trade['pnl']
    logging.info(f"[TRADE]: {trade}")
    _log_performance()


def _calculate_pnl(trade: Dict) -> float:
    if trade['direction'] == Sentiment.POSITIVE.name:
        return (trade['exit_price'] - trade['entry_price']) * trade['amount']
    elif trade['direction'] == Sentiment.NEGATIVE.name:
        return (trade['entry_price'] - trade['exit_price']) * trade['amount']
    return 0.0


def _log_performance():
    total_pnl = sum(trade['pnl'] for trade in trades if trade['pnl'] is not None)
    pnl_percentage = (current_capital / STARTING_CAPITAL) * 100
    win_ratio = _get_win_ratio()
    [formatted_total_pnl, formatted_pnl, formatted_win_ratio] = round_to_2dp(total_pnl, pnl_percentage, win_ratio)

    logging.info(f"[TRADE] Total trades made: {len(trades)}")
    logging.info(f"[TRADE] Total PnL: {formatted_total_pnl}")
    logging.info(f"[TRADE] Win Ratio: {formatted_win_ratio}%")
    logging.info(f"[TRADE] Performance: {formatted_pnl}%")


def _evaluate_result():
    if not trades:
        logging.info("[EVALUATION] No trades to evaluate.")
        return

    sorted_trades = sorted(trades, key=lambda trade: trade['pnl'], reverse=True)

    # Get top 10 gainers and losers
    top_gainers = sorted_trades[:10]
    top_losers = sorted_trades[-10:]

    logging.info("[EVALUATION] Top 10 Gainers:")
    for trade in top_gainers:
        logging.info(trade)

    logging.info("[EVALUATION] Top 10 Losers:")
    for trade in reversed(top_losers):  # Reverse to show the largest losses first
        logging.info(trade)


def _get_win_ratio() -> float:
    if not trades:
        return 0.0
    winning_trades = sum(1 for trade in trades if trade['pnl'] > 0)
    return winning_trades / len(trades) * 100
