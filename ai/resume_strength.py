# ai/resume_strength.py

def calculate_resume_strength(
    ats_score,
    detected_skills,
    section_report
):

    sections_present = sum(section_report.values())

    skill_count = len(detected_skills)

    if ats_score >= 90:
        level = "Excellent"
        stars = 5

    elif ats_score >= 75:
        level = "Advanced"
        stars = 4

    elif ats_score >= 60:
        level = "Intermediate"
        stars = 3

    elif ats_score >= 40:
        level = "Beginner"
        stars = 2

    else:
        level = "Needs Improvement"
        stars = 1

    return {
        "level": level,
        "stars": stars,
        "skills": skill_count,
        "sections": sections_present
    }