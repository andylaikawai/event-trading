import json

from utils.util import format_time, parse_datetime_to_timestamp

# input
RAW_ALL_NEWS_FILE = 'raw_all_news.json'
FROM_DATE = '20250301'
TO_DATE = '20250401'

# output
OUTPUT_FILE = f'raw_news_{FROM_DATE}_{TO_DATE}.json'

from_timestamp = parse_datetime_to_timestamp(FROM_DATE)
to_timestamp = parse_datetime_to_timestamp(TO_DATE)

# === Main Execution ===
if __name__ == "__main__":
    with open(RAW_ALL_NEWS_FILE, 'r') as file:
        raw_news = json.load(file)

    print(f"Total number of raw news events: {len(raw_news)}")
    print(f"Latest news: {format_time(raw_news[0].get('time'), '%Y%m%d %H:%M:%S')}")
    print(f"Oldest news: {format_time(raw_news[-1].get('time'), '%Y%m%d %H:%M:%S')}")
    print(f"Filtering news from {FROM_DATE} to {TO_DATE}")

    filtered_news = list(filter(lambda x: to_timestamp > x.get('time') >= from_timestamp, raw_news))

    print(f"Filtered news count: {len(filtered_news)}")

    with open(OUTPUT_FILE, "w") as file:
        json.dump(filtered_news, file, indent=4)


