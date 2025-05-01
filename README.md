# Tech Stack

- Python 3.9.6

# Install dependencies

- `pip install -r requirements.txt`

# How to use

- run `main.py` to start backtesting. See `config.py` for configuration. Output `.logs` files.

- (optional) run `data/data_preprocessor.py` to view historical data. see README.md in `data` folder for more details.

# TODO

#### For coding challenge:
- Decide exact requirements
- Decide evaluation metric
- GET API to serve preprocessed (a.k.a training) data
- GET API to serve test data (without performance results)
- POST API to evaluate trading decision and log submission?
- Add some hints for the challenge

#### For backtesting:
- improve win ratio to serve as a benchmark? currently ~60-80% depending on parameters for sentiment analysis