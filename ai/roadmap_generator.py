from ai.groq_service import ask_resume_ai

def generate_roadmap(skills):

    prompt = f"""
You are an experienced career mentor.

The candidate knows these skills:

{', '.join(skills)}

Create a 6-month learning roadmap.

Include:

Month 1
Month 2
Month 3
Month 4
Month 5
Month 6

Also recommend:

• Certifications
• Projects
• Interview Preparation
• Resources
"""

    return ask_resume_ai(prompt)