from transformers import pipeline

sentiment_model = pipeline("sentiment-analysis", model="ProsusAI/finbert")

def analyze_sentiment(news_list):
    results = sentiment_model(news_list)
    summary = {"positive": 0, "neutral": 0, "negative": 0}
    for r in results:
        summary[r["label"].lower()] += 1
    return summary, results
