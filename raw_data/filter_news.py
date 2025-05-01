import json

from utils.util import format_time, parse_datetime_to_timestamp

raw_all_news_file = './all_news.json'
period_in_months = 1
from_date = '2025-03-01'
to_date = '2025-04-01'

from_timestamp = parse_datetime_to_timestamp(from_date)
to_timestamp = parse_datetime_to_timestamp(to_date)

# === Main Execution ===
if __name__ == "__main__":
    with open(raw_all_news_file, 'r') as file:
        raw_news = json.load(file)

    print(f"Total number of raw news events: {len(raw_news)}")
    print(f"Latest news: {format_time(raw_news[0].get('time'))}")
    print(f"Oldest news: {format_time(raw_news[-1].get('time'))}")
    print(f"Filtering news from {from_date} to {to_date}")

    filtered_news = list(filter(lambda x: to_timestamp > x.get('time') >= from_timestamp, raw_news))

    print(f"Filtered news count: {len(filtered_news)}")

    with open(f"raw_news_{from_date}_{to_date}.json", "w") as file:
        json.dump(filtered_news, file)


