import os
import json

from dotenv import load_dotenv
from groq import Groq
from groq import RateLimitError

load_dotenv()

# =========================================================
# GROQ CONFIGURATION
# =========================================================

MODEL_NAME = "openai/gpt-oss-20b"

api_key = os.getenv("GROQ_API_KEY")

client = (
    Groq(
        api_key=api_key,
        max_retries=0
    )
    if api_key
    else None
)


# =========================================================
# SINGLE AI REQUEST
# =========================================================

def generate_all_ai_content(resume_text, detected_skills):
    """
    Generate all AI-powered resume features using ONE Groq API call.

    This prevents multiple sequential API calls from causing
    Groq rate-limit errors and Gunicorn worker timeouts.
    """

    default_response = {
        "ai_review": (
            "AI service is temporarily unavailable. "
            "Your resume was uploaded successfully. "
            "Please try the AI analysis again later."
        ),

        "interview_questions": (
            "AI service is temporarily unavailable. "
            "Please try again later."
        ),

        "cover_letter": (
            "AI service is temporarily unavailable. "
            "Please try again later."
        ),

        "rewritten_resume": (
            "AI service is temporarily unavailable. "
            "Please try again later."
        ),

        "roadmap": (
            "AI service is temporarily unavailable. "
            "Please try again later."
        )
    }

    # -----------------------------------------------------
    # Check API key
    # -----------------------------------------------------

    if not client:
        print("Groq AI Error: GROQ_API_KEY is not configured.")
        return default_response

    # -----------------------------------------------------
    # Create ONE combined prompt
    # -----------------------------------------------------

    skills_text = ", ".join(detected_skills)

    prompt = f"""
You are an expert ATS resume analyzer, technical interviewer,
career mentor, professional resume writer, and recruiter.

Analyze the candidate's resume below.

You must generate ALL of the following in ONE response.

=========================================================
SECTION 1 — AI RESUME REVIEW
=========================================================

Give:

1. Overall Resume Review
2. Strengths
3. Weaknesses
4. ATS Improvement Suggestions
5. Career Advice

=========================================================
SECTION 2 — INTERVIEW QUESTIONS
=========================================================

Generate:

1. Five Technical Interview Questions
2. Five HR Interview Questions
3. Three Project-based Questions

=========================================================
SECTION 3 — COVER LETTER
=========================================================

Write a modern, professional, ATS-friendly cover letter
based on the candidate's resume.

=========================================================
SECTION 4 — RESUME REWRITE
=========================================================

Rewrite the resume professionally.

Improve:

- Grammar
- ATS Keywords
- Bullet Points
- Professional Tone
- Clarity
- Impact

=========================================================
SECTION 5 — SIX-MONTH CAREER ROADMAP
=========================================================

Create a practical 6-month learning roadmap based on
the candidate's current skills.

Include:

Month 1
Month 2
Month 3
Month 4
Month 5
Month 6

Also include:

- Certifications
- Projects
- Interview Preparation
- Resources

=========================================================
IMPORTANT OUTPUT FORMAT
=========================================================

Use these exact markers:

### AI_REVIEW_START
Your resume review here
### AI_REVIEW_END

### INTERVIEW_START
Interview questions here
### INTERVIEW_END

### COVER_LETTER_START
Cover letter here
### COVER_LETTER_END

### REWRITE_START
Rewritten resume here
### REWRITE_END

### ROADMAP_START
Career roadmap here
### ROADMAP_END

Do not omit any section.

=========================================================
CANDIDATE SKILLS
=========================================================

{skills_text}

=========================================================
RESUME
=========================================================

{resume_text}
"""

    # -----------------------------------------------------
    # ONE API REQUEST ONLY
    # -----------------------------------------------------

    try:

        print("Sending ONE combined request to Groq...")

        response = client.chat.completions.create(
            model=MODEL_NAME,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.7,

            max_tokens=7000
        )

        content = response.choices[0].message.content

        print("Combined AI analysis completed successfully.")

        # -------------------------------------------------
        # Parse sections
        # -------------------------------------------------

        def extract_section(text, start_marker, end_marker):

            if start_marker not in text:
                return ""

            start = text.find(start_marker) + len(start_marker)

            end = text.find(end_marker, start)

            if end == -1:
                return text[start:].strip()

            return text[start:end].strip()

        ai_review = extract_section(
            content,
            "### AI_REVIEW_START",
            "### AI_REVIEW_END"
        )

        interview_questions = extract_section(
            content,
            "### INTERVIEW_START",
            "### INTERVIEW_END"
        )

        cover_letter = extract_section(
            content,
            "### COVER_LETTER_START",
            "### COVER_LETTER_END"
        )

        rewritten_resume = extract_section(
            content,
            "### REWRITE_START",
            "### REWRITE_END"
        )

        roadmap = extract_section(
            content,
            "### ROADMAP_START",
            "### ROADMAP_END"
        )

        # -------------------------------------------------
        # Fallback if a section wasn't parsed
        # -------------------------------------------------

        if not ai_review:
            ai_review = "AI resume review could not be generated."

        if not interview_questions:
            interview_questions = "Interview questions could not be generated."

        if not cover_letter:
            cover_letter = "Cover letter could not be generated."

        if not rewritten_resume:
            rewritten_resume = "Resume rewrite could not be generated."

        if not roadmap:
            roadmap = "Career roadmap could not be generated."

        return {
            "ai_review": ai_review,
            "interview_questions": interview_questions,
            "cover_letter": cover_letter,
            "rewritten_resume": rewritten_resume,
            "roadmap": roadmap
        }

    # -----------------------------------------------------
    # RATE LIMIT
    # -----------------------------------------------------

    except RateLimitError as e:

        print("Groq Rate Limit Error:", str(e))

        rate_message = (
            "AI service is temporarily busy due to API rate limits. "
            "Your resume was uploaded successfully, but the AI "
            "analysis could not be completed right now. "
            "Please try again later."
        )

        return {
            "ai_review": rate_message,
            "interview_questions": rate_message,
            "cover_letter": rate_message,
            "rewritten_resume": rate_message,
            "roadmap": rate_message
        }

    # -----------------------------------------------------
    # OTHER ERRORS
    # -----------------------------------------------------

    except Exception as e:

        print("Groq AI Error:", str(e))

        error_message = (
            "AI service is currently unavailable. "
            "Your resume was uploaded successfully, but the AI "
            "analysis could not be completed. Please try again later."
        )

        return {
            "ai_review": error_message,
            "interview_questions": error_message,
            "cover_letter": error_message,
            "rewritten_resume": error_message,
            "roadmap": error_message
        }


# =========================================================
# EXISTING SINGLE-PROMPT FUNCTION
# =========================================================

def ask_resume_ai(prompt):
    """
    Keep this function for other parts of the project
    that may still use ask_resume_ai().
    """

    if not client:
        print("Groq AI Error: GROQ_API_KEY is not configured.")

        return (
            "AI service is currently unavailable because "
            "the API key is not configured."
        )

    try:

        response = client.chat.completions.create(
            model=MODEL_NAME,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.7,

            max_tokens=4000
        )

        return response.choices[0].message.content

    except RateLimitError as e:

        print("Groq Rate Limit Error:", str(e))

        return (
            "AI service is temporarily busy due to API rate limits. "
            "Your resume was uploaded successfully, but this AI "
            "analysis is temporarily unavailable. Please try again later."
        )

    except Exception as e:

        print("Groq AI Error:", str(e))

        return (
            "AI service is currently unavailable. "
            "Your resume was uploaded successfully, but this AI "
            "analysis could not be completed. Please try again later."
        )