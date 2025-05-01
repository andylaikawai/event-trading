import logging

from trading.exchange import exchange
from model.candles import Candles
from model.sentiment import Sentiment


# FIXME 3 args
def live_trade(symbol: str, trade_amount: float, sentiment: Sentiment, candles: Candles):
    try:
        market = exchange.load_markets().get(symbol)
        if not market:
            logging.info(f"[TRADE] Symbol {symbol} not available.")
            return
    except Exception as e:
        logging.error(f"[TRADE] Trade Error: {e}")

    if sentiment == Sentiment.POSITIVE:
        order = exchange.create_market_buy_order(symbol, trade_amount)
        logging.info(f"[TRADE] BUY executed: {order['id']} | {symbol}")

    elif sentiment == Sentiment.NEGATIVE:
        order = exchange.create_market_sell_order(symbol, trade_amount)
        logging.info(f"[TRADE] SELL executed: {order['id']} | {symbol}")

    elif sentiment == Sentiment.NEUTRAL:
        logging.debug("[TRADE] Neutral sentiment detected. No trade executed.")