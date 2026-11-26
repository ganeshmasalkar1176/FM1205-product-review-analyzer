from collections import Counter

import numpy as np
import pandas as pd


POSITIVE_WORDS = {
    "excellent", "good", "great", "amazing", "love", "perfect", "works",
    "useful", "recommend", "quality", "fast", "best", "happy", "fine",
    "awesome", "satisfied",
}
NEGATIVE_WORDS = {
    "poor", "terrible", "hate", "waste", "broken", "bad", "disappointing",
    "stopped", "badly", "not", "problem", "slow", "useless", "worst",
}


def score_sentiment(tokens):
    positive_count = sum(1 for token in tokens if token in POSITIVE_WORDS)
    negative_count = sum(1 for token in tokens if token in NEGATIVE_WORDS)
    return float(positive_count - negative_count)


def analyse_reviews(data):
    if "tokens" not in data.columns:
        raise ValueError("Cleaned data must include a 'tokens' column")

    result = data.copy()
    result["sentiment_score"] = result["tokens"].apply(score_sentiment)
    result["sentiment_label"] = np.select(
        [result["sentiment_score"] > 0, result["sentiment_score"] < 0],
        ["Positive", "Negative"],
        default="Neutral",
    )
    result["is_mismatch"] = (
        ((result["rating"] >= 4) & (result["sentiment_score"] < 0))
        | ((result["rating"] <= 2) & (result["sentiment_score"] > 0))
    )

    word_counter = Counter(
        token
        for tokens in result["tokens"]
        for token in tokens
    )

    rating_counts = result["rating"].value_counts().sort_index()
    sentiment_by_product = (
        result.groupby("product", as_index=False)
        .agg(
            average_sentiment=("sentiment_score", "mean"),
            average_rating=("rating", "mean"),
            review_count=("review_text", "count"),
        )
        .sort_values("average_sentiment", ascending=False)
    )

    mismatch_count = int(result["is_mismatch"].sum())
    mismatch_percentage = round(mismatch_count / len(result) * 100, 2) if len(result) else 0.0

    return {
        "data": result,
        "word_counter": word_counter,
        "rating_counts": rating_counts,
        "sentiment_by_product": sentiment_by_product,
        "mismatch_count": mismatch_count,
        "mismatch_percentage": mismatch_percentage,
    }
