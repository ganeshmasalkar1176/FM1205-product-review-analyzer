import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


random.seed(42)

PRODUCTS = [
    ("Wireless Headphones", "Electronics"),
    ("Running Shoes", "Sports"),
    ("Coffee Maker", "Appliances"),
    ("Smart Watch", "Electronics"),
    ("Yoga Mat", "Fitness"),
]

POSITIVE = [
    "Excellent quality and very useful",
    "I absolutely love this product",
    "Great value for the price",
    "Works perfectly and arrived quickly",
    "Amazing performance, highly recommended",
]

NEGATIVE = [
    "Very poor quality and stopped working",
    "Terrible experience, I hate this item",
    "Waste of money and badly designed",
    "Broken on arrival and poor service",
    "Not useful and extremely disappointing",
]

NEUTRAL = [
    "It is okay for the price",
    "Average product with basic features",
    "Decent but could be better",
    "The item meets expectations",
]


def make_review(review_index):
    product, category = PRODUCTS[review_index % len(PRODUCTS)]
    sentiment_type = random.choices(
        ["positive", "negative", "neutral"], weights=[55, 25, 20]
    )[0]

    if sentiment_type == "positive":
        rating = random.randint(4, 5)
        text = random.choice(POSITIVE)
    elif sentiment_type == "negative":
        rating = random.randint(1, 2)
        text = random.choice(NEGATIVE)
    else:
        rating = random.randint(3, 3)
        text = random.choice(NEUTRAL)

    if random.random() < 0.22:
        rating = 5 if random.random() < 0.5 else 1

    if random.random() < 0.15:
        text = text.replace("Excellent", "sooo Excellent")
    if random.random() < 0.12:
        text += " Visit https://example.com"
    if random.random() < 0.12:
        text += " @reviewer"
    if random.random() < 0.08:
        text += " 😍😊"

    date = datetime(2025, 1, 1) + timedelta(days=random.randint(0, 364))
    return {
        "product": product,
        "category": category,
        "rating": rating,
        "date": date.strftime("%d-%m-%Y") if review_index % 4 == 0 else date.strftime("%Y-%m-%d"),
        "review_text": text,
    }


def generate_reviews(row_count=3000, output_path=None):
    rows = [make_review(index) for index in range(row_count)]
    output_path = output_path or Path(__file__).resolve().parent / "reviews.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output_path, index=False)
    print(f"Generated {row_count} reviews at {output_path}")


if __name__ == "__main__":
    generate_reviews()
