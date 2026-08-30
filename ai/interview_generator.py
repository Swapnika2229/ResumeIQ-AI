from ai.groq_service import ask_resume_ai

def generate_interview_questions(resume_text):

    prompt = f"""
You are an experienced technical interviewer.

Generate:

1. Five Technical Interview Questions
2. Five HR Interview Questions
3. Three Project-based Questions

Resume:

{resume_text}
"""

    return ask_resume_ai(prompt)