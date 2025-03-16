def analyze_sentiment(headline, content):
    prompt = f"""
    Determine sentiment (Positive, Negative, Neutral) for the following crypto news. Respond with ONE word only.

    Headline: {headline}
    Content: {content}
    Sentiment:
    """
    # To implement: Call to OpenAI or another sentiment analysis API
    return "Neutral"  # Placeholder return value