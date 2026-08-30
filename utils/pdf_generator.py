from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from xml.sax.saxutils import escape
import re


def clean_text(text):
    """Make text safe for ReportLab Paragraph."""
    if text is None:
        return ""

    text = str(text)

    # Remove unsupported HTML-like tags
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</?para>", "", text, flags=re.IGNORECASE)

    # Escape XML/HTML special characters
    text = escape(text)

    # Basic Markdown formatting
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", text)
    text = re.sub(r"`(.*?)`", r"<font name='Courier'>\1</font>", text)

    return text


def add_ai_review(story, ai_review, styles):
    """
    Convert AI Markdown-style output into ReportLab-safe elements.
    """

    if not ai_review:
        story.append(
            Paragraph("No AI review was generated.", styles["Normal"])
        )
        return

    lines = ai_review.splitlines()

    table_rows = []
    in_table = False

    for raw_line in lines:

        line = raw_line.strip()

        # Skip completely empty lines
        if not line:
            if in_table and table_rows:
                story.append(
                    create_table(table_rows)
                )
                table_rows = []
                in_table = False

            story.append(Spacer(1, 6))
            continue

        # Detect Markdown table
        if "|" in line:

            cells = [
                cell.strip()
                for cell in line.strip("|").split("|")
            ]

            # Ignore Markdown separator row
            if all(
                re.fullmatch(r":?-+:?", cell.replace(" ", ""))
                for cell in cells
            ):
                in_table = True
                continue

            table_rows.append(cells)
            in_table = True
            continue

        # Close previous table
        if in_table and table_rows:
            story.append(
                create_table(table_rows)
            )
            table_rows = []
            in_table = False

        # Markdown headings
        if line.startswith("### "):
            text = clean_text(line[4:])
            story.append(
                Paragraph(text, styles["Heading3"])
            )
            story.append(Spacer(1, 4))
            continue

        if line.startswith("## "):
            text = clean_text(line[3:])
            story.append(
                Paragraph(text, styles["Heading2"])
            )
            story.append(Spacer(1, 5))
            continue

        # Numbered section headings such as:
        # 1. Overall Resume Review
        if re.match(r"^\d+\.\s+\*\*.*\*\*", line):
            text = clean_text(line)
            story.append(
                Paragraph(text, styles["Heading2"])
            )
            story.append(Spacer(1, 5))
            continue

        # Bullet points
        if line.startswith("- ") or line.startswith("* "):
            text = clean_text(line[2:])
            story.append(
                Paragraph(
                    "• " + text,
                    styles["Normal"]
                )
            )
            continue

        # Numbered list
        if re.match(r"^\d+\.\s+", line):
            text = clean_text(line)
            story.append(
                Paragraph(text, styles["Normal"])
            )
            continue

        # Horizontal rule
        if line in ("---", "***", "___"):
            story.append(Spacer(1, 8))
            continue

        # Normal paragraph
        text = clean_text(line)

        if text:
            story.append(
                Paragraph(text, styles["Normal"])
            )

    # Add remaining table
    if table_rows:
        story.append(
            create_table(table_rows)
        )


def create_table(rows):
    """Create a simple, safe ReportLab table."""

    safe_rows = []

    for row in rows:
        safe_row = [
            Paragraph(
                clean_text(cell),
                getSampleStyleSheet()["Normal"]
            )
            for cell in row
        ]
        safe_rows.append(safe_row)

    table = Table(
        safe_rows,
        repeatRows=1
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    return table


def generate_pdf(
    filename,
    ats_score,
    skills,
    missing_skills,
    ai_review
):

    doc = SimpleDocTemplate(
        filename,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Improve normal text readability
    styles["Normal"].fontSize = 9
    styles["Normal"].leading = 13

    styles["Heading2"].spaceBefore = 10
    styles["Heading2"].spaceAfter = 6

    story = []

    # Title
    story.append(
        Paragraph(
            "<b>ResumeIQ AI Report</b>",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 12))

    # ATS Score
    story.append(
        Paragraph(
            f"<b>ATS Score:</b> {escape(str(ats_score))}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 8))

    # Detected Skills
    detected = ", ".join(
        str(skill) for skill in skills
    )

    story.append(
        Paragraph(
            f"<b>Detected Skills:</b> {escape(detected)}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 8))

    # Missing Skills
    missing = ", ".join(
        str(skill) for skill in missing_skills
    )

    story.append(
        Paragraph(
            f"<b>Missing Skills:</b> {escape(missing)}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 12))

    # AI Review Heading
    story.append(
        Paragraph(
            "<b>AI Resume Review</b>",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 6))

    # AI Review
    add_ai_review(
        story,
        ai_review,
        styles
    )

    # Build PDF
    doc.build(story)