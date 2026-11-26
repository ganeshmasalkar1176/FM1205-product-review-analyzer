import unittest

import pandas as pd

from src.analysis import analyse_reviews, score_sentiment


class AnalysisTests(unittest.TestCase):
    def test_sentiment_score(self):
        self.assertGreater(score_sentiment(["excellent", "great"]), 0)
        self.assertLess(score_sentiment(["poor", "broken"]), 0)
        self.assertEqual(score_sentiment(["product"]), 0)

    def test_mismatch_detection(self):
        data = pd.DataFrame({
            "product": ["Headphones", "Shoes"],
            "rating": [5, 1],
            "review_text": ["Poor broken", "Excellent product"],
            "tokens": [["poor", "broken"], ["excellent", "product"]],
        })
        result = analyse_reviews(data)
        self.assertEqual(result["mismatch_count"], 2)


if __name__ == "__main__":
    unittest.main()
