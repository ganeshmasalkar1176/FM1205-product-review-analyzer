import unittest

from src.cleaning import clean_text, parse_mixed_date, tokenize


class CleaningTests(unittest.TestCase):
    def test_clean_text_removes_url_mention_and_emoji(self):
        text = "Excellent @buyer! https://example.com 😍"
        cleaned = clean_text(text)
        self.assertNotIn("http", cleaned)
        self.assertNotIn("@buyer", cleaned)
        self.assertNotIn("😍", cleaned)

    def test_repeated_letters_are_normalized(self):
        self.assertEqual(clean_text("sooo good"), "so good")

    def test_tokenize_removes_stop_words(self):
        tokens = tokenize("This is a great and useful product")
        self.assertIn("great", tokens)
        self.assertIn("useful", tokens)
        self.assertNotIn("is", tokens)

    def test_mixed_date_parsing(self):
        first = parse_mixed_date("2025-03-15")
        second = parse_mixed_date("15-03-2025")
        self.assertFalse(first is None)
        self.assertFalse(second is None)
        self.assertEqual(first.strftime("%Y-%m-%d"), "2025-03-15")
        self.assertEqual(second.strftime("%Y-%m-%d"), "2025-03-15")


if __name__ == "__main__":
    unittest.main()
