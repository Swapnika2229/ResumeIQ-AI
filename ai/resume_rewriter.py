from ai.groq_service import ask_resume_ai

def rewrite_resume(resume_text):

    prompt = f"""
You are an expert resume writer.

Rewrite this resume professionally.

Improve:
- Grammar
- ATS Keywords
- Bullet Points
- Professional Tone

Resume:

{resume_text}
"""

    return ask_resume_ai(prompt)