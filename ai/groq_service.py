import os
import time

from dotenv import load_dotenv
from groq import Groq
from groq import RateLimitError

load_dotenv()

# Smaller model = lower token usage and faster responses
MODEL_NAME = "openai/gpt-oss-20b"

# Maximum amount of resume text sent to Groq.
# This prevents very large PDFs from exceeding Groq's TPM limit.
MAX_PROMPT_CHARS = 12000

# Keep output reasonably small.
MAX_OUTPUT_TOKENS = 1200

api_key = os.getenv("GROQ_API_KEY")

client = (
    Groq(
        api_key=api_key,
        max_retries=0
    )
    if api_key
    else None
)


def _limit_prompt(prompt):
    """
    Prevent extremely large prompts from being sent to Groq.
    """

    if not prompt:
        return ""

    if len(prompt) <= MAX_PROMPT_CHARS:
        return prompt

    print(
        f"Groq prompt truncated: "
        f"{len(prompt)} characters -> {MAX_PROMPT_CHARS}"
    )

    return (
        prompt[:MAX_PROMPT_CHARS]
        + "\n\n[Resume text truncated for AI processing.]"
    )


def ask_resume_ai(prompt):
    """
    Send a compact request to Groq.

    This function:
    - limits prompt size
    - limits output tokens
    - handles rate limits
    - handles oversized requests
    - never crashes the Flask application
    """

    if not client:
        print("Groq AI Error: GROQ_API_KEY is not configured.")

        return (
            "AI service is currently unavailable because the API key "
            "is not configured."
        )

    prompt = _limit_prompt(prompt)

    try:

        response = client.chat.completions.create(
            model=MODEL_NAME,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.4,

            max_tokens=MAX_OUTPUT_TOKENS
        )

        if not response.choices:
            return (
                "AI service returned an empty response. "
                "Please try again."
            )

        return response.choices[0].message.content

    except RateLimitError as e:

        error_text = str(e)

        print("Groq Rate Limit Error:", error_text)

        return (
            "AI service is temporarily busy because the Groq API "
            "rate limit has been reached. Your resume was uploaded "
            "successfully. Please wait about 30 seconds and try again."
        )

    except Exception as e:

        print("Groq AI Error:", error_text if "error_text" in locals() else str(e))

        return (
            "AI service is currently unavailable. "
            "Your resume was uploaded successfully, but the AI "
            "analysis could not be completed. Please try again later."
        )