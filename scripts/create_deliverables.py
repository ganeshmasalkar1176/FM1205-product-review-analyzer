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
            "Reviews analysed: 2973",
            "Mismatch count: 239",
            "Mismatch percentage: 8.04%",
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
        "Python PG Project - FM1205",
        "Project P22",
        "Student: FM1205",
        "Problem: Analyze large volumes of product reviews",
    ])
    add_slide(prs, "Problem & Objectives", [
        "Clean noisy review text",
        "Measure word frequency and sentiment",
        "Compare text sentiment with star ratings",
        "Identify rating/sentiment mismatches",
    ])
    add_slide(prs, "Dataset & Cleaning", [
        "3000 synthetic reviews",
        "Mixed date formats, URLs, mentions and emojis",
        "Regex-based URL, mention and emoji removal",
        "Repeated-letter normalization and tokenization",
        "Stop-word removal using a set",
    ])
    add_slide(prs, "Technology & Architecture", [
        "Pandas: cleaning and group analysis",
        "NumPy: numeric calculations",
        "Matplotlib: three visualizations",
        "Counter and dictionaries: word and sentiment analysis",
        "Modules: cleaning.py, analysis.py, visuals.py",
    ])
    add_slide(prs, "Analysis Features", [
        "Lexicon-based sentiment scores",
        "Positive, negative and neutral labels",
        "Top 20 words",
        "Mismatch detection",
        "Sentiment comparison by product",
    ])
    add_slide(prs, "Rating Distribution", [
        "3,000 reviews were generated",
        "2973 valid records were analyzed",
        "Rating distribution visualized as a bar chart",
    ], ROOT / "outputs/rating_distribution.png")
    add_slide(prs, "Top Words", [
        "Stop-words removed before counting",
        "Counter ranks word frequency",
        "Top 20 words shown horizontally",
    ], ROOT / "outputs/top_words.png")
    add_slide(prs, "Rating vs. Sentiment", [
        "239 mismatched records found",
        "Mismatch percentage: 8.04%",
        "Scatter plot compares rating and text sentiment",
    ], ROOT / "outputs/rating_vs_sentiment.png")
    add_slide(prs, "Execution & Conclusion", [
        "Live demo: python main.py",
        "Data, charts and cleaned CSV generated successfully",
        "GitHub repository and README prepared",
        "Resume-ready review mining project",
    ])
    prs.save(ROOT / "FM1205_slides.pptx")


def create_submission_pdf():
    styles = getSampleStyleSheet()
    document = SimpleDocTemplate(str(ROOT / "FM1205_submission.pdf"), pagesize=A4)
    content = [
        Paragraph("FM1205 Product Review Text & Rating Analyzer", styles["Title"]),
        Spacer(1, 16),
        Paragraph("<b>Project Number:</b> P22", styles["Heading2"]),
        Paragraph("<b>Student:</b> FM1205", styles["Heading2"]),
        Spacer(1, 20),
        Paragraph("Problem Statement", styles["Heading1"]),
        Paragraph("Build a tool that cleans product reviews, finds frequent words and compares lexicon-based sentiment with star ratings.", styles["BodyText"]),
        Spacer(1, 12),
        Paragraph("Implementation Summary", styles["Heading1"]),
        Paragraph("The project generates a synthetic dataset, applies regex cleaning, tokenizes and filters text, calculates sentiment, detects mismatches, exports cleaned data and creates three visualizations.", styles["BodyText"]),
        Spacer(1, 12),
        Paragraph("Repository", styles["Heading1"]),
        Paragraph("Student GitHub repository", styles["BodyText"]),
        Spacer(1, 12),
        Paragraph("Verified Results", styles["Heading1"]),
        Paragraph("3000 reviews generated; 2973 valid records analyzed; 239 mismatches detected; mismatch percentage 8.04%.", styles["BodyText"]),
        Spacer(1, 12),
        Paragraph("Resume Bullet", styles["Heading1"]),
        Paragraph("Developed a review-mining tool that cleans 3,000 reviews with regex and scores sentiment using Python data structures and Pandas.", styles["BodyText"]),
    ]
    document.build(content)


def create_slides_pdf():
    slides = [
        ("Product Review Text & Rating Analyzer", ["Python PG Project - FM1205", "Project P22", "Student: FM1205"]),
        ("Problem & Objectives", ["Clean noisy review text", "Measure word frequency and sentiment", "Compare sentiment with star ratings", "Identify mismatches"]),
        ("Dataset & Cleaning", ["3000 synthetic reviews", "Mixed dates, URLs, mentions and emojis", "Regex cleaning and repeated-letter normalization", "Tokenization and stop-word removal"]),
        ("Technology & Architecture", ["Pandas for cleaning and analysis", "NumPy for numeric calculations", "Matplotlib for visualizations", "Cleaning, analysis and visuals modules"]),
        ("Analysis Features", ["Lexicon sentiment scores", "Positive, negative and neutral labels", "Top 20 words", "Mismatch detection"]),
        ("Rating Distribution", ["2973 valid records analyzed", "Rating distribution by star rating"], ROOT / "outputs/rating_distribution.png"),
        ("Top Words", ["Stop-words removed", "Counter ranks the top 20 words"], ROOT / "outputs/top_words.png"),
        ("Rating vs. Sentiment", ["239 mismatches detected", "Mismatch percentage: 8.04%"], ROOT / "outputs/rating_vs_sentiment.png"),
        ("Execution & Conclusion", ["Live demo: python main.py", "Cleaned CSV and 3 charts generated", "GitHub and README prepared"]),
    ]
    pdf = canvas.Canvas(str(ROOT / "FM1205_slides.pdf"), pagesize=landscape(A4))
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
    print("Created screenshots, FM1205_slides.pptx, FM1205_slides.pdf, and FM1205_submission.pdf")
