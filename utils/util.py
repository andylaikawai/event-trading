import time


def format_time(timestamp_ms):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(timestamp_ms / 1000))