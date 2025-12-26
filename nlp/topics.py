def extract_topics(news_list):
    keywords = {
        "rates": "Interest Rates",
        "inflation": "Inflation",
        "earnings": "Earnings",
        "growth": "Growth",
        "value": "Valuation"
    }
    topics = []
    for text in news_list:
        for k, v in keywords.items():
            if k in text.lower():
                topics.append(v)
    return list(set(topics))
