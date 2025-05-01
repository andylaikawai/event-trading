import json

# input
from_date = '20250301'
to_date = '20250401'
coin = 'BTC'

raw_data_input_file = f'../raw_data/raw_news_{from_date}_{to_date}.json'

processed_data_output_file = f'./processed_news_{from_date}_{to_date}_{coin}.json'

def preprocess_news_data(input_file: str, output_file: str):
    with open(input_file, 'r') as file:
        raw_news = json.load(file)

    # Project only the specified keys
    processed_news = [
        {
            "title": news.get("title"),
            "time": news.get("time"),
            "url": news.get("url"),
            "source": news.get("source"),
        }
        for news in raw_news
        if any(suggestion.get("coin") == coin for suggestion in news.get("suggestions", []))
    ]

    with open(output_file, 'w') as file:
        json.dump(processed_news, file, indent=4)

if __name__ == "__main__":
    preprocess_news_data(raw_data_input_file, processed_data_output_file)
    print(f"Processed news data saved to {processed_data_output_file}")