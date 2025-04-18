import json

file_path = './news_data_20250418.json'
period_in_months = 3

# === Main Execution ===
if __name__ == "__main__":
    with open(file_path, 'r') as file:
        raw_news = json.load(file)

    last_timestamp = raw_news[0].get('time')
    until = last_timestamp - period_in_months * 30 * 24 * 60 * 60 * 1000
    filtered_news = list(filter(lambda x: x.get('time') >= until, raw_news))
    with open("news_data.json", "w") as file:
        json.dump(filtered_news, file)
