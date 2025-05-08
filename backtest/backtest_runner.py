import logging

from backtest.post_trade_analysis import post_trade_analysis, log_performance, get_roi_percent, log_top_trades
from backtest.sentiment_analysis import analyze_sentiment
from config import STARTING_CAPITAL, SYMBOL
from data.scripts.data_preprocessor import get_preprocessed_news
from logger import display_news
from model.candles import Candle, Candles
from model.news_event import HistoricalNewsEvent
from model.sentiment import Sentiment
from model.trade_params import TradeParams
from utils.util import round_to_2dp, min_to_ms

MAX_NUMBER_OF_TRADES = 99999

current_capital = STARTING_CAPITAL
trades: list[dict] = []


def run_backtest(params: TradeParams) -> float:
    news_data = get_preprocessed_news()

    for news_event in news_data:
        if len(trades) >= MAX_NUMBER_OF_TRADES:
            logging.info(f"Reached the maximum number of trades: {MAX_NUMBER_OF_TRADES}")
            break
        _historical_news_event_handler(params, news_event)

    log_top_trades(trades)
    return get_roi_percent(current_capital)


def _historical_news_event_handler(params: TradeParams, news_event: HistoricalNewsEvent):
    try:
        display_news(news_event)

        # TODO let's not hardcode symbol here
        symbol = SYMBOL
        sentiment = analyze_sentiment(params, news_event, symbol)

        # FIXME it is unfair to analyse future data and trade at an older timestamp, this is for illustration purpose only
        execution_candle = news_event.observation_candles[0]
        # execution_candle = news_event.observation_candles[-1]

        _paper_trade(params, symbol, sentiment, execution_candle, news_event.performance_candles)

        post_trade_analysis(news_event)

    except Exception as e:
        logging.error(f"[ERROR] Processing Error: {e}")


def _paper_trade(params: TradeParams, symbol: str, sentiment: Sentiment, candle: Candle, performance_candles: Candles):
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
    _exit_trade(params, trade, performance_candles)


def _get_exit_candle(params: TradeParams, trade: dict, candles: Candles, exit_time: int) -> Candle:
    entry_price = trade['entry_price']
    direction = trade['direction']

    for candle in candles:
        if candle.timestamp >= exit_time:
            logging.info(f"[TRADE] Exit time reached")
            return candle

        gain = (candle.close - entry_price) / entry_price
        if direction == Sentiment.NEGATIVE.name:
            gain *= -1
        if gain >= params.take_profit:
            logging.info(f"[TRADE] Take profit")
            return candle
        if gain <= params.stop_loss:
            logging.info(f"[TRADE] Stop loss")
            return candle

    raise ValueError(f"Not enough performance candles ({len(candles)}) to hold trade for {params.max_holding_period} minutes. Refresh raw candle data")


def _exit_trade(params: TradeParams, trade: dict, candles: Candles):
    global current_capital

    exit_time = trade['entry_time'] + min_to_ms(params.max_holding_period)
    entry_price = trade['entry_price']
    exit_candle = _get_exit_candle(params, trade, candles, exit_time)

    exit_price = exit_candle.close
    price_change_percent = ((exit_price - entry_price) / entry_price) * 100
    trade['exit_price'] = exit_price
    trade['exit_time'] = exit_candle.timestamp
    trade['price_change_percent'] = round_to_2dp(price_change_percent)[0]
    trade['pnl'] = round_to_2dp(_calculate_pnl(trade))[0]
    current_capital += trade['pnl']
    logging.info(f"[TRADE]: {trade}")
    log_performance(trades, current_capital)


def _calculate_pnl(trade: dict) -> float:
    if trade['direction'] == Sentiment.POSITIVE.name:
        return (trade['exit_price'] - trade['entry_price']) * trade['amount']
    elif trade['direction'] == Sentiment.NEGATIVE.name:
        return (trade['entry_price'] - trade['exit_price']) * trade['amount']
    return 0.0