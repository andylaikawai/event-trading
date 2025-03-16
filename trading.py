import ccxt
from config import KUCOIN_API_KEY, KUCOIN_SECRET, KUCOIN_PASSPHRASE, DEFAULT_TRADE_AMOUNT

# Initialize exchange
exchange = ccxt.kucoin({
    'apiKey': KUCOIN_API_KEY,
    'secret': KUCOIN_SECRET,
    'password': KUCOIN_PASSPHRASE,
    'enableRateLimit': True,
})

def make_trade(symbol, sentiment):
    trade_amount = DEFAULT_TRADE_AMOUNT
    try:
        market = exchange.load_markets().get(symbol)
        if not market:
            print(f"Symbol {symbol} not available on KuCoin.")
            return

        if sentiment == "Positive":
            order = exchange.create_market_buy_order(symbol, trade_amount)
            print(f"📈 BUY executed: {order['id']} | {symbol}")

        elif sentiment == "Negative":
            order = exchange.create_market_sell_order(symbol, trade_amount)
            print(f"📉 SELL executed: {order['id']} | {symbol}")

        else:
            print("😐 Neutral sentiment detected. No trade executed.")

    except Exception as e:
        print(f"Trade Error: {e}")