# Setup guide

## Tech Stack

- Python 3.9.6

## Install dependencies

- `pip install -r requirements.txt`

## How to use

- run `main.py` to start backtesting. See `config.py` for configuration. Output `.logs` files.

- (optional) run `data/data_preprocessor.py` to view historical data. see README.md in `data` folder for more details.

# Coding challenge

## Description

The goal of the coding challenge is to build a crypto trading bot that takes in a list of 1000 news event and
associated historical Bitcoin price data as the input, and outputs 10 selected news event with respective trading
decisions (`LONG` or `SHORT`)

For example, given below input:

```json
[
  {
    "id": 1,
    "title": "db (@tier10k): *TRUMP SIGNS EXECUTIVE ORDER TO ESTABLISH STRATEGIC BITCOIN RESERVE: SACKS",
    "time": 1741306326681,
    "url": "https://twitter.com/tier10k/status/1897802400632648066",
    "source": "Twitter",
    "previous_candles": [
      {
        "timestamp": 1741306200000,
        "open": 89886.67,
        "high": 89961.27,
        "low": 89878.51,
        "close": 89960.51,
        "volume": 4.85351,
        "datetime": "2025-03-07 08:10:00"
      },
      {
        "timestamp": 1741306260000,
        "open": 89960.52,
        "high": 90229.97,
        "low": 89932.45,
        "close": 90218.6,
        "volume": 62.09979,
        "datetime": "2025-03-07 08:11:00"
      },
      {
        "timestamp": 1741306320000,
        "open": 90218.59,
        "high": 90595.72,
        "low": 90208.24,
        "close": 90591.18,
        "volume": 93.9068,
        "datetime": "2025-03-07 08:12:00"
      }
    ],
    "observation_candles": [
      {
        "timestamp": 1741306380000,
        "open": 90591.19,
        "high": 91283.02,
        "low": 90591.19,
        "close": 91123.95,
        "volume": 278.03794,
        "datetime": "2025-03-07 08:13:00"
      },
      {
        "timestamp": 1741306440000,
        "open": 91123.94,
        "high": 91212.0,
        "low": 90218.0,
        "close": 90218.0,
        "volume": 218.40361,
        "datetime": "2025-03-07 08:14:00"
      },
      {
        "timestamp": 1741306500000,
        "open": 90218.0,
        "high": 90420.0,
        "low": 88300.0,
        "close": 89218.58,
        "volume": 720.8261,
        "datetime": "2025-03-07 08:15:00"
      }
    ]
  }
  // ... +999 other news events
]
```

The bot should output:

```json
[
  {
    "id": 1,
    "decision": "SHORT"
  }
  //  ...+9 other trading decisions 
]
```

with the assumption that, for each trading decision:

1. `id` corresponds to the unique id of the news event from input
2. Each trade will be entered at the `close` price of the first candle of `observation_candles` (e.g. "91123.95" at "
   2025-03-07 08:13:00" in the above example)
3. Each trade will be exited 30 minutes after the trade is executed (e.g. "2025-03-07 08:43:00" in the above example,
   exit price is hidden from the bot)

The evaluation server will check whether each decision is correct or not, and return a maximum of 10 points (1 point for
each correct decision) to the bot.

"Correctness" is defined as follows:

- if exit price is higher than the entry price, then the correct decision is LONG
- if exit price is lower than the entry price, then the correct decision is SHORT

Using the above example, the evaluation server has the knowledge that for this particular trade, the exit
price is 86118.67 at 2025-03-07 08:43:00. Therefore, the SHORT decision is correct, and the bot will return:

```json
[
  {
    "id": 1,
    "correct": true
  }
  //  ...+9 other results
]
```

## Hints

First, let's have a basic understanding of Candlestick: https://en.wikipedia.org/wiki/Candlestick_chart

To detect if a news event has triggered a significant market movement (positive or negative momentum) and decide whether
your trading bot should place a trade, you need a robust way to measure and interpret the market's reaction to the
event. Below are some simple the steps and techniques you can use to build an accurate detection mechanism:

1. Define Thresholds for Significant Market Movement

   Percentage Price Change: Set a threshold for percentage price change. For example, if the price moves up or down by
   more than a certain percentage within the 3-minute window after the news event, there is likely significant momentum.
   Implementation:

2. Volume Analysis
   Spike in Trading Volume: News-driven momentum is often accompanied by a significant increase in trading volume.
   Compare the volume of `observation_candles` to the average of historical volumes (i.e. `previous_candles`).
   For example, if the volume exceeds 2x or 3x the historical volume, it may confirm the market's reaction to the news.

Pick top 10 trades using above simple technique should already give a good win rate (70+%)

Optionally, techniques that may improve the accuracy include Natural Language Processing (NLP) for News Sentiment. The
bot may include a sentiment analysis component to determine if the news itself is bullish or bearish before analyzing
the market reaction. This helps filter out news that might not have a clear directional impact. Example tools for
sentiment analysis include Pre-trained NLP models (e.g., BERT or OpenAI's GPT-based models).

# TODO

#### For coding challenge:

- GET API to serve preprocessed (a.k.a training) data
- GET API to serve test data (without performance results)
- POST API to evaluate trading decision and log submission?

#### For backtesting:

- improve win ratio to serve as a benchmark? currently ~60-80% depending on parameters for sentiment analysis