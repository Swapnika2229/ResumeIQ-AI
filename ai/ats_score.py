# ai/ats_score.py

def calculate_ats_score(text, detected_skills):

    score = 0
    suggestions = []

    text_lower = text.lower()

    # Contact Information
    if "@" in text:
        score += 10
    else:
        suggestions.append("Add a professional email address.")

    # Phone Number
    digits = sum(c.isdigit() for c in text)
    if digits >= 10:
        score += 10
    else:
        suggestions.append("Add a valid phone number.")

    # Education
    if "education" in text_lower:
        score += 10
    else:
        suggestions.append("Add an Education section.")

    # Skills
    if "skills" in text_lower:
        score += 10
    else:
        suggestions.append("Add a Skills section.")

    # Projects
    if "project" in text_lower:
        score += 15
    else:
        suggestions.append("Add Projects to strengthen your resume.")

    # Experience
    if "experience" in text_lower:
        score += 15
    else:
        suggestions.append("Include internships or experience.")

    # Certifications
    if "certification" in text_lower or "certifications" in text_lower:
        score += 10
    else:
        suggestions.append("Add your certifications.")

    # Technical Skills
    skill_score = min(len(detected_skills) * 2, 20)
    score += skill_score

    if len(detected_skills) < 5:
        suggestions.append("Include more relevant technical skills.")

    score = min(score, 100)

    return score, suggestions