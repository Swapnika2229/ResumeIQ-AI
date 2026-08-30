from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_report(
    filename,
    ats_score,
    detected_skills,
    suggestions,
    career_advice,
    predicted_roles,
    resume_strength,
    ai_review,
    interview_questions,
    cover_letter,
    rewritten_resume,
    roadmap,
    job_match
):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>ResumeIQ AI Report</b>", styles["Title"]))

    story.append(Paragraph(f"ATS Score : {ats_score}%", styles["Normal"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph("<b>Detected Skills</b>", styles["Heading2"]))

    story.append(
        Paragraph(", ".join(detected_skills), styles["Normal"])
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(
        Paragraph("<b>AI Suggestions</b>", styles["Heading2"])
    )

    for s in suggestions:

        story.append(
            Paragraph("• " + s, styles["Normal"])
        )

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(
        Paragraph("<b>Career Advice</b>", styles["Heading2"])
    )

    for advice in career_advice:

        story.append(
            Paragraph("• " + advice, styles["Normal"])
        )

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(
        Paragraph("<b>Recommended Job Roles</b>", styles["Heading2"])
    )

    for role, percent in predicted_roles:

        story.append(
            Paragraph(
                f"{role} : {percent}%",
                styles["Normal"]
            )
        )

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(
        Paragraph(
            "<b>Resume Level : "
            + resume_strength["level"]
            + "</b>",
            styles["Heading2"]
        )
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(
        Paragraph("<b>Resume vs Job Match</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(f"{job_match}%", styles["Normal"])
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(
        Paragraph("<b>AI Resume Review</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(ai_review.replace("\n","<br/>"), styles["Normal"])
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(
        Paragraph("<b>Interview Questions</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(
            interview_questions.replace("\n","<br/>"),
            styles["Normal"]
        )
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(
        Paragraph("<b>Cover Letter</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(
            cover_letter.replace("\n","<br/>"),
            styles["Normal"]
        )
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(
        Paragraph("<b>AI Resume Rewrite</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(
            rewritten_resume.replace("\n","<br/>"),
            styles["Normal"]
        )
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(
        Paragraph("<b>Career Roadmap</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(
            roadmap.replace("\n","<br/>"),
            styles["Normal"]
        )
    )

    doc.build(story)