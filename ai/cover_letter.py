from ai.groq_service import ask_resume_ai

def generate_cover_letter(resume_text):

    prompt = f"""
You are a professional HR recruiter.

Write a modern, ATS-friendly cover letter based on this resume.

Resume:

{resume_text}
"""

    return ask_resume_ai(prompt)