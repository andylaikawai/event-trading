# Usage

Run `data_preprocess.py` to preprocess raw news data downloaded and stored in `raw_data` directory.

## Input

See scripts input section, i.e.:

```
FROM_DATE
TO_DATE
COIN
RAW_DATA_INPUT_FILE
``` 

## Output

A json file `preprocessed_news_[FROM_DATE]_[TO_DATE]_[COIN].json` will be generated in the same directory.

For each news item, given the time of the news, the script will populate:

- necessary fields for the news item (e.g. title, time, url, source)
- previous candles: 3 minutes prior to the news timestamp, for sentiment analysis purpose
- observation candles: 3 minutes after the news timestamp, for sentiment analysis purpose (e.g. observe whether the price / volume changes after the news)
- performance candles: 30 minutes after the news timestamp, for performance evaluation purpose only. Should not be used
  for sentiment analysis.

Sample

```
[
  {
    "title": "CoinDesk (@CoinDesk): As countries like the U.S. and El Salvador buy bitcoin for their reserves, yours should too, says @anuragarjun @AvailProject. \n\nOpinion. \n\ntrib.al/JUwmSVt",
    "time": 1743435398844,
    "url": "https://twitter.com/CoinDesk/status/1906732376517955771",
    "source": "Twitter",
    "previous_candles": [
      [
        1743435240000,
        83739.9,
        83739.9,
        83652.8,
        83661.8,
        1.745632,
        "2025-03-31 23:34:00"
      ],
      ...
      [
        1743435360000,
        83641.5,
        83685.5,
        83540.6,
        83540.6,
        1.38621996,
        "2025-03-31 23:36:00"
      ]
    ],
    "observation_candles": [
      [
        1743435420000,
        83547.0,
        83610.1,
        83547.0,
        83575.6,
        0.55174547,
        "2025-03-31 23:37:00"
      ],
      ...
      [
        1743435540000,
        83582.9,
        83615.1,
        83539.6,
        83539.6,
        0.76424132,
        "2025-03-31 23:39:00"
      ]
    ],
    "performance_candles": [
      [
        1743435420000,
        83547.0,
        83610.1,
        83547.0,
        83575.6,
        0.55174547,
        "2025-03-31 23:37:00"
      ],
      ...
      [
        1743437160000,
        83579.7,
        83614.5,
        83571.7,
        83594.0,
        1.37906947,
        "2025-04-01 00:06:00"
      ]
    ]
  },
  ...
]
```



