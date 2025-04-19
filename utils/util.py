import time


def format_time(timestamp_ms):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(1744971600686 / 1000))

def min_to_ms(minutes: int) -> int:
    return minutes * 60 * 1000

def round_to_2dp(*values):
    return [round(value, 2) for value in values]