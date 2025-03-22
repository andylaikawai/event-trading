import logging

import ccxt
import requests
from typing import Union

from backtest.back_test import paper_trade
from config import KUCOIN_API_KEY, KUCOIN_SECRET, KUCOIN_PASSPHRASE, DEFAULT_TRADE_AMOUNT, is_backtest_mode
from type.type import Sentiment, Candles

# Initialize exchange
exchange = ccxt.kucoin({
    'apiKey': KUCOIN_API_KEY,
    'secret': KUCOIN_SECRET,
    'password': KUCOIN_PASSPHRASE,
    'enableRateLimit': True,
})


def execute_trade_based_on_signals(symbol: str, timestamp: int):
    sentiment = _get_sentiment(symbol, timestamp)
    _make_trade(symbol, sentiment)


def _make_trade(symbol: str, sentiment: Sentiment):
    trade_amount = DEFAULT_TRADE_AMOUNT
    trade_executor = paper_trade if is_backtest_mode else _live_trade
    trade_executor(symbol, trade_amount, sentiment)


def _live_trade(symbol: str, trade_amount: float, sentiment: Sentiment):
    try:
        market = exchange.load_markets().get(symbol)
        if not market:
            logging.info(f"[TRADE] Symbol {symbol} not available on KuCoin.")
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
        logging.info("[TRADE] Neutral sentiment detected. No trade executed.")


def _get_sentiment(symbol: str, timestamp: int) -> Sentiment:
    candles = _fetch_market_price(symbol, timestamp)
    if candles is None:
        return Sentiment.NEUTRAL

    current_candle = candles[0]
    previous_candle = candles[1]
    current_close = float(current_candle[2])  # Close price of the current minute
    previous_close = float(previous_candle[2])  # Close price of the previous minute

    if current_close > previous_close * 1.001:
        logging.info(f"[TRADE] Positive sentiment detected for {symbol}.")
        return Sentiment.POSITIVE
    elif current_close < previous_close * 0.999:
        logging.info(f"[TRADE] Negative sentiment detected for {symbol}.")
        return Sentiment.NEGATIVE
    else:
        return Sentiment.NEUTRAL


# see doc at https://www.kucoin.com/docs/rest/spot-trading/market-data/get-klines
def _fetch_market_price(symbol: str, timestamp: int) -> Union[Candles, None]:
    """Fetch the market price from KuCoin at a specific timestamp."""
    # Convert timestamp to seconds
    timestamp_seconds = timestamp / 1000
    start_time = int(timestamp_seconds - 120)  # 2 minutes before the news timestamp
    end_time = int(timestamp_seconds)  # At the news timestamp

    # Fetch historical market data with a 1-minute interval
    url = f'https://api.kucoin.com/api/v1/market/candles?type=1min&symbol={symbol}-USDT&startAt={start_time}&endAt={end_time}'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['code'] == '200000' and len(data['data']) >= 2:
            return data['data']

    else:
        print(f'Failed to fetch market price with response: {response}')
        return None
