import logging

from backtest.post_trade_analysis import post_trade_analysis
from backtest.sentiment_analysis import analyze_sentiment
from config import STARTING_CAPITAL, TAKE_PROFIT, STOP_LOSS, SYMBOL
from data.scripts.data_preprocessor import get_preprocessed_news
from logger import display_news
from model.candles import Candle, Candles
from model.news_event import HistoricalNewsEvent
from model.sentiment import Sentiment
from utils.util import round_to_2dp

MAX_NUMBER_OF_TRADES = 99999

current_capital = STARTING_CAPITAL
trades: list[dict] = []


def run_backtest() -> float:
    news_data = get_preprocessed_news()
    for news_event in news_data:
        if len(trades) >= MAX_NUMBER_OF_TRADES:
            logging.info(f"Reached the maximum number of trades: {MAX_NUMBER_OF_TRADES}")
            break
        _on_historical_news_event(news_event)
    _log_top_trades()
    return _get_roi()


def _on_historical_news_event(news_event: HistoricalNewsEvent):
    try:
        display_news(news_event)
        sentiment = analyze_sentiment(news_event)

        # FIXME it is unfair to analyse future data and trade at an older timestamp, this is for illustration purpose only
        execution_candle = news_event.observation_candles[0]
        # execution_candle = news_event.observation_candles[-1]

        paper_trade(SYMBOL, sentiment, execution_candle, news_event.performance_candles)

        post_trade_analysis(news_event)

    except Exception as e:
        logging.error(f"[ERROR] Processing Error: {e}")


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


def _get_exit_candle(trade: dict, candles: Candles, exit_time: int) -> Candle:
    entry_price = trade['entry_price']
    direction = trade['direction']

    for candle in candles:
        if candle.timestamp >= exit_time:
            logging.info(f"[TRADE] Exit time reached")
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


def _exit_trade(trade: dict, candles: Candles, minutes: int = 30):
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


def _calculate_pnl(trade: dict) -> float:
    if trade['direction'] == Sentiment.POSITIVE.name:
        return (trade['exit_price'] - trade['entry_price']) * trade['amount']
    elif trade['direction'] == Sentiment.NEGATIVE.name:
        return (trade['entry_price'] - trade['exit_price']) * trade['amount']
    return 0.0


def _get_roi():
    if current_capital == 0:
        return 0.0
    return (current_capital - STARTING_CAPITAL) / STARTING_CAPITAL * 100


def _get_evaluation_result():
    total_pnl = sum(trade['pnl'] for trade in trades if trade['pnl'] is not None)
    return_on_investment = _get_roi()
    win_ratio = _get_win_ratio()
    return total_pnl, return_on_investment, win_ratio


def _log_performance():
    [total_pnl, return_on_investment, win_ratio] = _get_evaluation_result()
    [formatted_total_pnl, formatted_roi, formatted_win_ratio] = round_to_2dp(total_pnl, return_on_investment, win_ratio)

    logging.info(f"[TRADE] Total trades made: {len(trades)}")
    logging.info(f"[TRADE] Total PnL: {formatted_total_pnl}")
    logging.info(f"[TRADE] Win Ratio: {formatted_win_ratio}%")
    logging.info(f"[TRADE] ROI: {formatted_roi}%")


def _log_top_trades():
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
