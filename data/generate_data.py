import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


random.seed(1205)

PRODUCTS = [
    ("Bluetooth Speaker", "Audio"),
    ("Trail Running Shoes", "Footwear"),
    ("Electric Kettle", "Kitchen"),
    ("Fitness Tracker", "Wearables"),
    ("Office Keyboard", "Computer Accessories"),
]

POSITIVE = [
    "Excellent sound and very useful",
    "I absolutely love this item",
    "Great quality at a fair price",
    "Works perfectly and arrived fast",
    "Amazing performance, highly recommended",
]

NEGATIVE = [
    "Very poor build and stopped working",
    "Terrible experience, I hate this product",
    "Waste of money and badly manufactured",
    "Broken on arrival with poor service",
    "Not useful and extremely disappointing",
]

NEUTRAL = [
    "It is fine for everyday use",
    "Average item with standard features",
    "Decent but could improve",
    "The product meets basic expectations",
]


def make_review(review_index):
    product, category = PRODUCTS[review_index % len(PRODUCTS)]
    sentiment_type = random.choices(
        ["positive", "negative", "neutral"], weights=[48, 28, 24]
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

    date = datetime(2026, 1, 1) + timedelta(days=random.randint(0, 364))
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
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output_path, index=False)
    print(f"Generated {row_count} reviews at {output_path}")


if __name__ == "__main__":
    generate_reviews()
