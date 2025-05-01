from typing import Optional

import ccxt

from model.candles import Candles, Candle

# Initialize exchange
exchange = ccxt.binance({
    # 'apiKey': BINANCE_API_KEY,
    # 'secret': BINANCE_SECRET,
    # 'password': BINANCE_PASSPHRASE,
    'enableRateLimit': True,
})


def fetch_candles_from_exchange(symbol: str, from_timestamp: int, to_timestamp: int = None,
                                number_of_candles: int = None) -> Optional[Candles]:
    params = {
        'paginate': True,
        'since': from_timestamp,
        'until': to_timestamp,
        'paginationCalls': 100
    }
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1m', since=from_timestamp,
                                 limit=number_of_candles, params=params)
    return [Candle.from_ohlcv(candle) for candle in ohlcv]
