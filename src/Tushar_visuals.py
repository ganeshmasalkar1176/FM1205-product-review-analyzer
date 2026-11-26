from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def save_rating_distribution(rating_counts, output_path):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(rating_counts.index.astype(str), rating_counts.values, color="#4C78A8")
    ax.set(title="Rating Distribution", xlabel="Star Rating", ylabel="Number of Reviews")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def save_top_words(word_counter, output_path, top_n=20):
    top_words = word_counter.most_common(top_n)
    words = [item[0] for item in reversed(top_words)]
    counts = [item[1] for item in reversed(top_words)]

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.barh(words, counts, color="#F58518")
    ax.set(title=f"Top {top_n} Most Frequent Words", xlabel="Frequency", ylabel="Word")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def save_rating_sentiment_scatter(data, output_path):
    fig, ax = plt.subplots(figsize=(8, 6))
    scatter = ax.scatter(
        data["rating"],
        data["sentiment_score"],
        c=data["sentiment_score"],
        cmap="coolwarm",
        alpha=0.55,
        edgecolors="none",
    )
    ax.axhline(0, color="gray", linestyle="--", linewidth=1)
    ax.set(title="Rating vs. Sentiment", xlabel="Star Rating", ylabel="Sentiment Score")
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.grid(alpha=0.2)
    fig.colorbar(scatter, ax=ax, label="Sentiment")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def create_visualizations(results, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    paths = {
        "rating_distribution": output_dir / "rating_distribution.png",
        "top_words": output_dir / "top_words.png",
        "rating_vs_sentiment": output_dir / "rating_vs_sentiment.png",
    }
    save_rating_distribution(results["rating_counts"], paths["rating_distribution"])
    save_top_words(results["word_counter"], paths["top_words"])
    save_rating_sentiment_scatter(results["data"], paths["rating_vs_sentiment"])
    return paths
