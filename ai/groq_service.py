import os

from dotenv import load_dotenv
from groq import Groq
from groq import RateLimitError

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

# Use the smaller and faster GPT-OSS model.
# It is a better fit for ResumeIQ AI's multiple AI features.
MODEL_NAME = "openai/gpt-oss-20b"

# Create the client only when an API key exists.
client = (
    Groq(
        api_key=api_key,
        max_retries=0,
        timeout=30.0
    )
    if api_key
    else None
)


def ask_resume_ai(prompt):
    """
    Send a prompt to Groq.

    The function is designed so that an AI/API failure
    does not crash the ResumeIQ application.
    """

    if not client:
        print("Groq AI Error: GROQ_API_KEY is not configured.")

        return (
            "AI service is currently unavailable because the "
            "GROQ_API_KEY is not configured."
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

            temperature=0.5,

            # Keep responses reasonably small so that one upload
            # does not consume excessive tokens.
            max_tokens=2000
        )

        if not response.choices:
            print("Groq AI Error: Empty response received.")

            return (
                "AI service returned an empty response. "
                "Please try again later."
            )

        answer = response.choices[0].message.content

        if not answer:
            print("Groq AI Error: Empty AI message.")

            return (
                "AI service returned an empty response. "
                "Please try again later."
            )

        return answer.strip()

    except RateLimitError as e:
        print("Groq Rate Limit Error:", str(e))

        return (
            "AI service is temporarily busy due to API rate limits. "
            "Your resume was uploaded successfully, but this AI "
            "analysis is temporarily unavailable. Please try again later."
        )

    except Exception as e:
        print("Groq AI Error:", repr(e))

        return (
            "AI service is currently unavailable. "
            "Your resume was uploaded successfully, but this AI "
            "analysis could not be completed. Please try again later."
        )