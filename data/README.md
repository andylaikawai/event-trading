# Usage

Run `scripts/data_preprocess.py` to preprocess raw news data downloaded and stored in `data` directory.

## Input

See `config.py`, mainly to specify:

```
FROM_DATE
TO_DATE
COIN
``` 

## Output

A json file `preprocessed_news_[FROM_DATE]_[TO_DATE]_[COIN].json` will be generated in the same directory.

For each news item, given the time of the news, the script will populate:

- necessary fields for the news item (e.g. title, time, url, source)
- previous candles: 3 minutes prior to the news timestamp, for sentiment analysis purpose
- observation candles: 3 minutes after the news timestamp, for sentiment analysis purpose (e.g. observe whether the
  price / volume changes after the news)
- performance candle: 30 minutes after the news timestamp, for performance evaluation purpose only. Should not be used
  for sentiment analysis.

#### Sample
Given the following configuration:

```python
NUMBER_OF_PREVIOUS_CANDLES = 3
NUMBER_OF_OBSERVATION_CANDLES = 3
NUMBER_OF_PERFORMANCE_CANDLES = 30
```

```json
{
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
  ],
  "performance_candles": [
    {
      "timestamp": 1741306380000,
      "open": 90591.19,
      "high": 91283.02,
      "low": 90591.19,
      "close": 91123.95,
      "volume": 278.03794,
      "datetime": "2025-03-07 08:13:00"
    },
    //   ...
    {
      "timestamp": 1741308300000,
      "open": 85918.14,
      "high": 85918.14,
      "low": 85519.56,
      "close": 85594.34,
      "volume": 242.43206,
      "datetime": "2025-03-07 08:45:00"
    }
  ]
}
```



