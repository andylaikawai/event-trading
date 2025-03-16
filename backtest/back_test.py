import json
import time

file_path = 'backtest/news_data.json'

def load_historical_news():

    with open(file_path, 'r') as file:
        return json.load(file)

def run_backtest(news_data, on_historical_message):
    """Run backtesting using historical news data."""
    for news_event in news_data:
        message = json.dumps(news_event)  # Simulate a received message
        on_historical_message(None, message)  # Call the existing on_message function

trades = []  # Store trades made during backtesting

def paper_trade(symbol, direction, amount):
    """Simulate a trade without executing it."""
    trade = {
        'symbol': symbol,
        'direction': direction,
        'amount': amount,
        'timestamp': time.time()
    }
    trades.append(trade)
    print(f"Paper traded: {trade}")

def evaluate_results():
    """Evaluate performance of trades made during backtesting."""
    # Add your evaluation logic here
    print("Evaluating backtest results...")
    print(f"Total trades made: {len(trades)}")
    # Additional metrics can be calculated here (e.g., profit/loss)