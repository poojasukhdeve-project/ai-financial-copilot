def sentiment_score(summary):
    total = sum(summary.values())
    if total == 0:
        return 0
    return (summary["positive"] - summary["negative"]) / total
