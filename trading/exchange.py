import ccxt

# Initialize exchange
exchange = ccxt.binance({
    # 'apiKey': BINANCE_API_KEY,
    # 'secret': BINANCE_SECRET,
    # 'password': BINANCE_PASSPHRASE,
    'enableRateLimit': True,
})


def fetch_candles_from_exchange(symbol: str, from_timestamp: int, to_timestamp: int = None) -> list[list]:
    params = {
        'paginate': True,
        'until': to_timestamp,
        'paginationCalls': 100
    }
    return exchange.fetch_ohlcv(symbol, timeframe='1m', since=from_timestamp, params=params)
