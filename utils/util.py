from datetime import datetime


def format_time(timestamp_ms):
    return datetime.fromtimestamp(timestamp_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')

def parse_datetime_to_timestamp(date: str, date_time_format: str = '%Y-%m-%d') -> int:
    return int(datetime.strptime(date, date_time_format).timestamp() * 1000)

def min_to_ms(minutes: int) -> int:
    return minutes * 60 * 1000

def round_to_2dp(*values):
    return [round(value, 2) for value in values]