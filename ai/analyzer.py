from ai.resume_parser import extract_text_from_pdf
from ai.skill_extractor import (
    extract_skills,
    categorize_skills,
    missing_skills
)
from ai.ats_score import calculate_ats_score
from ai.career_coach import generate_career_advice
from ai.job_roles import predict_job_roles
from ai.section_analyzer import analyze_sections
from ai.resume_strength import calculate_resume_strength


def analyze_resume(filepath):

    extracted_text = extract_text_from_pdf(filepath)

    detected_skills = extract_skills(extracted_text)

    categorized = categorize_skills(detected_skills)

    missing = missing_skills(detected_skills)

    ats_score, suggestions = calculate_ats_score(
        extracted_text,
        detected_skills
    )

    career_advice = generate_career_advice(
        detected_skills
    )

    predicted_roles = predict_job_roles(
        detected_skills
    )

    section_report = analyze_sections(
        extracted_text
    )

    resume_strength = calculate_resume_strength(
        ats_score,
        detected_skills,
        section_report
    )

    return {

        "text": extracted_text,

        "skills": detected_skills,

        "categorized": categorized,

        "missing": missing,

        "ats_score": ats_score,

        "suggestions": suggestions,

        "career": career_advice,

        "roles": predicted_roles,

        "sections": section_report,

        "strength": resume_strength

    }