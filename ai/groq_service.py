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
    Generate all AI resume features using ONE small Groq request.

    The resume is truncated and the output token limit is kept low
    to stay safely below Groq's free-tier TPM limit.
    """

    default_message = (
        "AI service is temporarily unavailable. "
        "Your resume was uploaded successfully, but the AI analysis "
        "could not be completed. Please try again later."
    )

    default_response = {
        "ai_review": default_message,
        "interview_questions": default_message,
        "cover_letter": default_message,
        "rewritten_resume": default_message,
        "roadmap": default_message
    }

    if not client:
        print("Groq AI Error: GROQ_API_KEY is not configured.")
        return default_response

    # ---------------------------------------------------------
    # LIMIT INPUT SIZE
    # ---------------------------------------------------------

    # Keep the resume small enough for the 8,000 TPM limit.
    resume_text = (resume_text or "").strip()

    if len(resume_text) > 9000:
        resume_text = resume_text[:9000] + "\n[Resume text truncated]"

    skills_text = ", ".join(detected_skills[:30])

    # ---------------------------------------------------------
    # SMALL COMBINED PROMPT
    # ---------------------------------------------------------

    prompt = f"""
You are an ATS resume expert and career mentor.

Analyze this candidate's resume and return FIVE concise sections.

1. AI RESUME REVIEW
Give:
- Overall review
- 3 strengths
- 3 weaknesses
- 5 ATS suggestions
- brief career advice

2. INTERVIEW QUESTIONS
Give:
- 5 technical questions
- 5 HR questions
- 3 project questions

3. COVER LETTER
Write a concise professional ATS-friendly cover letter.

4. RESUME REWRITE
Rewrite the important resume content professionally.
Keep it concise. Do not invent experience.

5. CAREER ROADMAP
Give a practical 6-month roadmap.
Include certifications, projects, interview preparation and resources.

Use EXACTLY these markers:

### AI_REVIEW_START
...
### AI_REVIEW_END

### INTERVIEW_START
...
### INTERVIEW_END

### COVER_LETTER_START
...
### COVER_LETTER_END

### REWRITE_START
...
### REWRITE_END

### ROADMAP_START
...
### ROADMAP_END

Candidate skills:{skills_text}

Resume:{resume_text}
"""

    # ---------------------------------------------------------
    # ONE SMALL API REQUEST
    # ---------------------------------------------------------

    try:
        print("Sending optimized combined request to Groq...")

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.5,
            max_tokens=3500
        )

        content = response.choices[0].message.content or ""

        print("Combined AI analysis completed successfully.")

        # -----------------------------------------------------
        # SECTION PARSER
        # -----------------------------------------------------

        def extract_section(text, start_marker, end_marker):
            start_index = text.find(start_marker)

            if start_index == -1:
                return ""

            start_index += len(start_marker)

            end_index = text.find(end_marker, start_index)

            if end_index == -1:
                return text[start_index:].strip()

            return text[start_index:end_index].strip()

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

        return {
            "ai_review": ai_review or "AI resume review could not be generated.",
            "interview_questions": (
                interview_questions
                or "Interview questions could not be generated."
            ),
            "cover_letter": (
                cover_letter
                or "Cover letter could not be generated."
            ),
            "rewritten_resume": (
                rewritten_resume
                or "Resume rewrite could not be generated."
            ),
            "roadmap": (
                roadmap
                or "Career roadmap could not be generated."
            )
        }

    except RateLimitError as e:
        print("Groq Rate Limit Error:", str(e))

        rate_message = (
            "AI service is temporarily busy because the AI usage limit "
            "was reached. Your resume was uploaded successfully. "
            "Please try again shortly."
        )

        return {
            "ai_review": rate_message,
            "interview_questions": rate_message,
            "cover_letter": rate_message,
            "rewritten_resume": rate_message,
            "roadmap": rate_message
        }

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