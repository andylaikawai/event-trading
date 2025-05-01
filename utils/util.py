import json
from datetime import datetime


def format_time(timestamp_ms: int, date_time_format: str = '%Y-%m-%d %H:%M:%S') -> str:
    return datetime.fromtimestamp(timestamp_ms / 1000).strftime(date_time_format)


def parse_datetime_to_timestamp(date: str, date_time_format: str = '%Y%m%d') -> int:
    return int(datetime.strptime(date, date_time_format).timestamp() * 1000)


def min_to_ms(minutes: int) -> int:
    return minutes * 60 * 1000


def round_to_2dp(*values):
    return [round(value, 2) for value in values]


def read_from_cache_or_fetch(file_path: str, fetch_function, *args, indent=None):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Cache file not found. Fetching data by {fetch_function.__name__}...")
        data = fetch_function(*args)
        if not data:
            raise ValueError(f"Failed to fetch data by {fetch_function.__name__} with arguments: {args}")
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=indent)
        return data
