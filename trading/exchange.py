import ccxt

from config import KUCOIN_API_KEY, KUCOIN_SECRET, KUCOIN_PASSPHRASE

# Initialize exchange
exchange = ccxt.kucoin({
    # 'apiKey': KUCOIN_API_KEY,
    # 'secret': KUCOIN_SECRET,
    # 'password': KUCOIN_PASSPHRASE,
    'enableRateLimit': True,
})