from pathlib import Path

import pandas as pd

from data.generate_data import generate_reviews
from src.analysis import analyse_reviews
from src.cleaning import clean_reviews
from src.visuals import create_visualizations


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_PATH = PROJECT_ROOT / "data" / "reviews.csv"
CLEANED_PATH = PROJECT_ROOT / "outputs" / "cleaned_reviews.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs"


def main():
    if not DATA_PATH.exists():
        generate_reviews(output_path=DATA_PATH)

    cleaned = clean_reviews(DATA_PATH)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(CLEANED_PATH, index=False)

    results = analyse_reviews(cleaned)
    chart_paths = create_visualizations(results, OUTPUT_DIR)

    print("\n=== Product Review Analysis Summary ===")
    print(f"Reviews analysed: {len(cleaned)}")
    print(f"Mismatch count: {results['mismatch_count']}")
    print(f"Mismatch percentage: {results['mismatch_percentage']}%")
    print("\nSentiment by product:")
    print(results["sentiment_by_product"].to_string(index=False))
    print("\nGenerated charts:")
    for name, path in chart_paths.items():
        print(f"- {name}: {path}")


if __name__ == "__main__":
    main()
