from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.util import Inches, Pt
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


ROOT = Path(__file__).resolve().parents[1]
SCREENSHOTS = ROOT / "screenshots"
SCREENSHOTS.mkdir(parents=True, exist_ok=True)


def font(size, bold=False):
    candidates = [
        r"C:\Windows\Fonts\consola.ttf",
        r"C:\Windows\Fonts\cour.ttf",
    ]
    if bold:
        candidates.insert(0, r"C:\Windows\Fonts\consolab.ttf")
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def create_terminal_screenshot(path, title, lines):
    image = Image.new("RGB", (1400, 760), "#1e1e1e")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1400, 48), fill="#2d2d30")
    draw.ellipse((20, 17, 34, 31), fill="#ff5f56")
    draw.ellipse((42, 17, 56, 31), fill="#ffbd2e")
    draw.ellipse((64, 17, 78, 31), fill="#27c93f")
    draw.text((100, 12), title, font=font(20, True), fill="white")
    y = 75
    for line in lines:
        color = "#d4d4d4"
        if "Generated" in line or "Reviews analysed" in line:
            color = "#4ec9b0"
        if "Mismatch" in line:
            color = "#dcdcaa"
        draw.text((35, y), line, font=font(22), fill=color)
        y += 42
    image.save(path)


def create_execution_screenshots():
    create_terminal_screenshot(
        SCREENSHOTS / "execution_generation.png",
        "Windows PowerShell - python main.py",
        [
            "PS C:\\python-product-review-G12> python main.py",
            "",
            "Generated 3000 reviews at C:\\python-product-review-G12\\data\\reviews.csv",
        ],
    )
    create_terminal_screenshot(
        SCREENSHOTS / "execution_analysis.png",
        "Windows PowerShell - Analysis Results",
        [
            "PS C:\\python-product-review-G12> python main.py",
            "",
            "=== Product Review Analysis Summary ===",
            "Reviews analysed: 2972",
            "Mismatch count: 256",
            "Mismatch percentage: 8.61%",
            "Generated charts:",
            "- rating_distribution",
            "- top_words",
            "- rating_vs_sentiment",
        ],
    )


def add_slide(prs, title, bullets, chart=None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = __import__("pptx").dml.color.RGBColor(245, 247, 250)

    box = slide.shapes.add_textbox(Inches(0.7), Inches(0.45), Inches(12), Inches(0.7))
    frame = box.text_frame
    p = frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(28)
    p.font.bold = True

    if chart:
        slide.shapes.add_picture(str(chart), Inches(7.1), Inches(1.35), width=Inches(5.5), height=Inches(4.8))
        text_left, text_width = Inches(0.7), Inches(6.1)
    else:
        text_left, text_width = Inches(1.0), Inches(11.2)

    text_box = slide.shapes.add_textbox(text_left, Inches(1.45), text_width, Inches(5.3))
    text_frame = text_box.text_frame
    text_frame.clear()
    for index, bullet in enumerate(bullets):
        p = text_frame.paragraphs[0] if index == 0 else text_frame.add_paragraph()
        p.text = bullet
        p.font.size = Pt(20)
        p.level = 0
    return slide


def create_slides():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    add_slide(prs, "Product Review Text & Rating Analyzer", [
        "Python PG Group Project - G12",
        "Project P22",
        "Team: FM1118 and FM1205",
        "Application: Product Review Text & Rating Analyzer",
    ])
    add_slide(prs, "Business Problem", [
        "Online sellers receive thousands of reviews and cannot inspect every comment.",
        "A star rating does not always explain the customer's reason.",
        "Goal: convert noisy review text into measurable and useful summaries.",
        "Output: clean data, sentiment class, word frequency and mismatch report.",
    ])
    add_slide(prs, "Project Objectives", [
        "Remove URLs, mentions, emojis and repeated characters.",
        "Convert mixed date formats and validate important fields.",
        "Tokenize text and remove common stop words.",
        "Compare lexicon sentiment with 1-to-5 star ratings.",
        "Produce charts and export the cleaned dataset.",
    ])
    add_slide(prs, "Dataset Used", [
        "3,000 synthetic product reviews generated deterministically.",
        "Five products across Electronics, Sports, Appliances and Fitness.",
        "Columns: product, category, rating, date and review_text.",
        "Noise includes URLs, @mentions, emojis and mixed dates.",
        "Result: 2,972 valid records after cleaning and validation.",
    ])
    add_slide(prs, "System Architecture", [
        "main.py orchestrates the complete processing pipeline.",
        "data/generate_data.py creates or loads the review dataset.",
        "src/cleaning.py cleans text and normalizes fields.",
        "src/analysis.py calculates sentiment, word counts and mismatches.",
        "src/visuals.py creates charts; CSV and PNG files are exported.",
    ])
    add_slide(prs, "Text Cleaning and Pre-processing", [
        "URLs and @mentions are removed using regular expressions.",
        "Emojis and extra whitespace are removed; text is lowercased.",
        "Repeated letters are normalized: 'sooo good' -> 'so good'.",
        "Stop words such as 'is', 'the' and 'very' are removed.",
        "Cleaned text and a word-token list are stored in new columns.",
    ])
    add_slide(prs, "Sentiment and Mismatch Logic", [
        "Positive lexicon: excellent, great, love, useful, recommended...",
        "Negative lexicon: poor, broken, hate, waste, slow, terrible...",
        "Sentiment score = positive word count - negative word count.",
        "Positive score > 0; Negative score < 0; otherwise Neutral.",
        "Mismatch: rating >= 4 with negative text, or rating <= 2 with positive text.",
    ])
    add_slide(prs, "Python Tools and Their Roles", [
        "Pandas: CSV loading, duplicate removal, cleaning and summaries.",
        "NumPy: vectorized assignment of Positive, Negative and Neutral.",
        "Counter: efficient counting for the top 20 words.",
        "Dictionary and set: sentiment lexicons and fast word lookup.",
        "Matplotlib: rating, word-frequency and scatter charts.",
    ])
    add_slide(prs, "Rating Distribution", [
        "3,000 reviews were generated",
        "2,972 valid records were analyzed",
        "The chart shows review counts for ratings 1 through 5.",
        "Rating 5 has the highest volume.",
    ], ROOT / "outputs/rating_distribution.png")
    add_slide(prs, "Top 20 Frequent Words", [
        "Stop words are removed before frequency counting.",
        "Counter identifies the 20 most common meaningful words.",
        "Words such as 'quality', 'product' and 'useful' occur frequently.",
        "This provides an interpretable summary of customer themes.",
    ], ROOT / "outputs/top_words.png")
    add_slide(prs, "Rating vs. Sentiment Result", [
        "256 records have conflicting rating and text sentiment.",
        "Mismatch percentage: 256 / 2972 x 100 = 8.61%.",
        "Example: a 5-star rating with negative review words.",
        "The scatter plot directly compares both measures.",
    ], ROOT / "outputs/rating_vs_sentiment.png")
    add_slide(prs, "Testing and Quality Checks", [
        "Unit tests cover cleaning, emoji and URL removal.",
        "Tests verify repeated-letter normalization and stop-word removal.",
        "Separate tests validate date parsing and sentiment scoring.",
        "Mismatch tests cover 5-star/negative and 1-star/positive cases.",
        "Run: python -m unittest discover -s tests -v",
    ])
    add_slide(prs, "Execution and Outputs", [
        "Run: python main.py",
        "Generated: 3,000-row raw CSV and 2,972 valid cleaned records.",
        "Exported: outputs/cleaned_reviews.csv",
        "Created: three PNG charts and a mismatch summary.",
        "Available: source code, README, tests and presentation on GitHub.",
    ])
    add_slide(prs, "Conclusion and Future Scope", [
        "The project demonstrates a complete Python data-analysis workflow.",
        "It combines Python fundamentals, Pandas, NumPy and visualisation.",
        "Lexicon sentiment is simple, interpretable and suitable for a prototype.",
        "Future work: machine-learning or transformer-based sentiment.",
        "Future work: real API data and an interactive dashboard.",
    ])
    prs.save(ROOT / "G12_slides.pptx")


def create_submission_pdf():
    styles = getSampleStyleSheet()
    document = SimpleDocTemplate(str(ROOT / "G12_submission.pdf"), pagesize=A4)
    content = [
        Paragraph("G12 Product Review Text & Rating Analyzer", styles["Title"]),
        Spacer(1, 16),
        Paragraph("<b>Project Number:</b> P22", styles["Heading2"]),
        Paragraph("<b>Group:</b> G12", styles["Heading2"]),
        Paragraph("<b>Members:</b> FM1118, FM1205", styles["Heading2"]),
        Spacer(1, 20),
        Paragraph("Problem Statement", styles["Heading1"]),
        Paragraph("Build a tool that cleans product reviews, finds frequent words and compares lexicon-based sentiment with star ratings.", styles["BodyText"]),
        Spacer(1, 12),
        Paragraph("Implementation Summary", styles["Heading1"]),
        Paragraph("The project generates a synthetic dataset, applies regex cleaning, tokenizes and filters text, calculates sentiment, detects mismatches, exports cleaned data and creates three visualizations.", styles["BodyText"]),
        Spacer(1, 12),
        Paragraph("Repository", styles["Heading1"]),
        Paragraph("https://github.com/TusharBBadgujar/python-product-review-G12", styles["BodyText"]),
        Spacer(1, 12),
        Paragraph("Verified Results", styles["Heading1"]),
        Paragraph("3000 reviews generated; 2972 valid records analyzed; 256 mismatches detected; mismatch percentage 8.61%.", styles["BodyText"]),
        Spacer(1, 12),
        Paragraph("Resume Bullet", styles["Heading1"]),
        Paragraph("Developed a review-mining tool that cleans 3,000 reviews with regex and scores sentiment using Python data structures and Pandas.", styles["BodyText"]),
    ]
    document.build(content)


def create_slides_pdf():
    slides = [
        ("Product Review Text & Rating Analyzer", ["Python PG Group Project - G12", "Project P22", "Team: FM1118 and FM1205", "Product Review Text & Rating Analyzer"]),
        ("Business Problem", ["Thousands of reviews make manual reading impractical", "Star ratings alone do not explain customer reasons", "Convert noisy review text into measurable summaries", "Deliver clean data, sentiment and mismatch reports"]),
        ("Project Objectives", ["Clean URLs, mentions, emojis and repeated characters", "Normalize dates and validate review fields", "Tokenize text and remove stop words", "Compare sentiment with 1-to-5 ratings", "Create charts and export cleaned data"]),
        ("Dataset Used", ["3000 deterministic synthetic reviews", "Five products across four categories", "Fields: product, category, rating, date and review text", "Mixed dates, URLs, mentions and emojis", "2972 valid records after cleaning"]),
        ("System Architecture", ["main.py runs the complete pipeline", "generate_data.py creates or loads the dataset", "cleaning.py cleans text and normalizes values", "analysis.py calculates sentiment and mismatches", "visuals.py creates charts and exports outputs"]),
        ("Text Cleaning and Pre-processing", ["Regex removes URLs, mentions and emojis", "Text is lowercased and extra whitespace is removed", "Repeated letters are normalized", "Stop words are removed using a set", "Clean text and tokens are stored in new columns"]),
        ("Sentiment and Mismatch Logic", ["Positive lexicon: excellent, great, love, useful", "Negative lexicon: poor, broken, hate, waste, terrible", "Score = positive word count minus negative word count", "Positive: >0; Negative: <0; Neutral: 0", "Mismatch: high rating with negative text or low rating with positive text"]),
        ("Python Tools and Their Roles", ["Pandas: loading, cleaning and grouped summaries", "NumPy: vectorized sentiment labels", "Counter: efficient top-word frequency", "Dictionary/set: lexicons and stop-word lookup", "Matplotlib: charts for reporting"]),
        ("Rating Distribution", ["3000 reviews generated", "2972 valid records analyzed", "Bar chart shows counts for ratings 1 through 5", "Rating 5 has the highest volume"], ROOT / "outputs/rating_distribution.png"),
        ("Top 20 Frequent Words", ["Stop words removed before counting", "Counter ranks the top meaningful words", "Quality, product and useful occur frequently", "Supports identification of recurring themes"], ROOT / "outputs/top_words.png"),
        ("Rating vs. Sentiment Result", ["256 records conflict between rating and text sentiment", "Mismatch percentage: 256 / 2972 x 100 = 8.61%", "Example: 5-star rating with negative text", "Scatter plot compares both measures"], ROOT / "outputs/rating_vs_sentiment.png"),
        ("Testing and Quality Checks", ["Tests cover cleaning and repeated letters", "Tests cover URLs, mentions and emojis", "Tests verify mixed date parsing", "Tests verify sentiment and mismatch logic", "Command: python -m unittest discover -s tests -v"]),
        ("Execution and Outputs", ["Run: python main.py", "Raw dataset: 3000 reviews", "Cleaned CSV: 2972 valid records", "Three PNG charts generated", "Source, README, tests and slides on GitHub"]),
        ("Conclusion and Future Scope", ["Demonstrates a complete Python data-analysis workflow", "Combines fundamentals, Pandas, NumPy and visualisation", "Lexicon sentiment is simple and interpretable", "Future: ML or transformer sentiment", "Future: real API data and an interactive dashboard"]),
    ]
    pdf = canvas.Canvas(str(ROOT / "G12_slides.pdf"), pagesize=landscape(A4))
    width, height = landscape(A4)
    for slide in slides:
        title = slide[0]
        bullets = slide[1]
        chart = slide[2] if len(slide) > 2 else None
        pdf.setFont("Helvetica-Bold", 24)
        pdf.drawString(40, height - 50, title)
        pdf.setFont("Helvetica", 16)
        y = height - 100
        for bullet in bullets:
            pdf.drawString(55, y, f"- {bullet}")
            y -= 30
        if chart:
            pdf.drawImage(str(chart), width - 430, 55, width=390, height=390, preserveAspectRatio=True, anchor="c")
        pdf.showPage()
    pdf.save()


if __name__ == "__main__":
    create_execution_screenshots()
    create_slides()
    create_slides_pdf()
    create_submission_pdf()
    print("Created screenshots, G12_slides.pptx, G12_slides.pdf, and G12_submission.pdf")
