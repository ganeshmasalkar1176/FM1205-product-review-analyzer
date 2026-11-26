import re
from pathlib import Path

import pandas as pd


URL_PATTERN = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
MENTION_PATTERN = re.compile(r"(?<!\w)@\w+", re.ASCII)
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\u2600-\u26FF"
    "\u2700-\u27BF"
    "]",
    re.UNICODE,
)
REPEATED_LETTER_PATTERN = re.compile(r"(.)\1{2,}", re.DOTALL)
WORD_PATTERN = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
DATE_PATTERN = re.compile(r"^(?:\d{4}-\d{2}-\d{2}|\d{2}-\d{2}-\d{4})$")

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from",
    "had", "has", "have", "i", "in", "is", "it", "of", "on", "or", "so",
    "the", "this", "to", "very", "was", "with", "very",
}


def clean_text(text):
    text = "" if pd.isna(text) else str(text)
    text = URL_PATTERN.sub(" ", text)
    text = MENTION_PATTERN.sub(" ", text)
    text = EMOJI_PATTERN.sub(" ", text)
    text = REPEATED_LETTER_PATTERN.sub(r"\1", text)
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text


def tokenize(text):
    return [word for word in WORD_PATTERN.findall(clean_text(text)) if word not in STOP_WORDS]


def parse_mixed_date(value):
    text = "" if pd.isna(value) else str(value).strip()
    if not DATE_PATTERN.match(text):
        return pd.NaT
    for date_format in ("%Y-%m-%d", "%d-%m-%Y"):
        try:
            return pd.to_datetime(text, format=date_format)
        except ValueError:
            continue
    return pd.NaT


def clean_reviews(input_path):
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Reviews dataset not found: {input_path}")

    data = pd.read_csv(input_path)
    required = {"product", "rating", "date", "review_text"}
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    data = data.drop_duplicates(subset=["product", "rating", "review_text", "date"])
    data["clean_text"] = data["review_text"].apply(clean_text)
    data["tokens"] = data["clean_text"].apply(tokenize)
    data["date"] = data["date"].apply(parse_mixed_date)
    data["rating"] = pd.to_numeric(data["rating"], errors="coerce")
    data = data.dropna(subset=["rating", "date", "clean_text"])
    data = data[data["clean_text"].str.strip().ne("")]
    data["rating"] = data["rating"].clip(1, 5).astype(int)
    return data.reset_index(drop=True)
