import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)


def ask_resume_ai(prompt):

    try:

        response = client.chat.completions.create(

            model="openai/gpt-oss-120b",

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

    except Exception as e:

        print("Groq AI Error:", str(e))

        return "AI service is currently unavailable. Please try again later."