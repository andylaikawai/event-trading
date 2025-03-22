from enum import Enum
from typing import List, Tuple

Candle = Tuple[str, str, str, str, str, str]  # Define a custom type for a candle
Candles = List[Candle]  # Define a custom type for a list of candles

class Sentiment(Enum):
    POSITIVE = "Positive"
    NEGATIVE = "Negative"
    NEUTRAL = "Neutral"