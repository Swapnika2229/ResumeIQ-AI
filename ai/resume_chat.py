from ai.groq_service import ask_resume_ai


def chat_with_resume(resume_text, question):

    if not resume_text:
        return "No resume was found. Please upload your resume again."

    if not question:
        return "Please enter a question."

    prompt = f"""
You are ResumeIQ AI, an intelligent resume assistant.

Analyze the user's resume and answer their question clearly and professionally.

RESUME:
{resume_text}

USER QUESTION:
{question}

Give a useful answer based specifically on the resume.
If the question asks how to improve something, give practical suggestions.
Do not say that you cannot access the resume.

Answer:
"""

    print("=== RESUME CHAT START ===")
    print("Question:", question)
    print("Resume length:", len(resume_text))

    answer = ask_resume_ai(prompt)

    print("AI ANSWER:")
    print(answer)
    print("=== RESUME CHAT END ===")

    return answer