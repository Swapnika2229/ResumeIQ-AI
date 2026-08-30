import os
import sqlite3
from flask import Flask, render_template, request, send_file, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from ai.analyzer import analyze_resume
from ai.groq_service import ask_resume_ai
from ai.interview_generator import generate_interview_questions
from ai.cover_letter import generate_cover_letter
from ai.job_match import calculate_job_match
from ai.resume_rewriter import rewrite_resume
from ai.roadmap_generator import generate_roadmap
from ai.resume_chat import chat_with_resume
from database.database import (
    create_tables,
    get_resume_by_id,
    get_latest_resume,
    update_chat_answer
)
from utils.email_sender import send_report
from utils.pdf_generator import generate_pdf

from dotenv import load_dotenv
from email_config import configure_mail

load_dotenv()

app = Flask(__name__)
app.secret_key = "resumeiq_secret_key"

configure_mail(app)

# Initialize database tables
create_tables()

# Ensure uploads folder exists
os.makedirs("uploads", exist_ok=True)


@app.route("/")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("resumeiq.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM resume_history
        WHERE user_id=?
        ORDER BY upload_date DESC
        LIMIT 1
    """, (session["user_id"],))

    latest_resume = cursor.fetchone()

    conn.close()

    if latest_resume:
        ats_score = latest_resume["ats_score"]
        skills_count = latest_resume["skills_count"]
        job_matches = latest_resume["job_matches"]
        resume_rating = latest_resume["resume_rating"]
    else:
        ats_score = 0
        skills_count = 0
        job_matches = 0
        resume_rating = "N/A"

    return render_template(
        "dashboard.html",
        username=session["user_name"],
        ats_score=ats_score,
        skills_count=skills_count,
        job_matches=job_matches,
        resume_rating=resume_rating
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        password_raw = request.form.get("password")

        if not fullname or not email or not password_raw:
            return render_template(
                "register.html",
                error="Please fill in all form fields."
            )

        password = generate_password_hash(password_raw)

        conn = sqlite3.connect("resumeiq.db")
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO users (fullname, email, password)
                VALUES (?, ?, ?)
                """,
                (fullname, email, password)
            )
            conn.commit()
            conn.close()

            return render_template(
                "login.html",
                success="Registration Successful! Please Login."
            )
        except sqlite3.Error:
            conn.close()
            return render_template(
                "register.html",
                error="Email already exists."
            )

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        conn = sqlite3.connect("resumeiq.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            session["user_id"] = user[0]
            session["user_name"] = user[1]
            session["user_email"] = user[2]
            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid Email or Password"
        )

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/upload", methods=["GET", "POST"])
def upload():

    if "user_id" not in session:
        return redirect(url_for("login"))

    # Show upload page normally
    if request.method == "GET":
        return render_template(
            "upload.html",
            extracted_text="",
            detected_skills=[],
            categorized={},
            missing=[],
            ats_score=0,
            suggestions=[],
            career_advice=[],
            predicted_roles=[],
            section_report={},
            resume_strength={},
            ai_review="",
            interview_questions="",
            job_match=0,
            cover_letter="",
            rewritten_resume="",
            roadmap="",
            chat_answer="",
            pdf_file=""
        )

    # =========================
    # POST - RESUME UPLOAD
    # =========================

    print("POST request received")

    resume = request.files.get("resume")

    print("Resume object:", resume)

    # Check whether file was selected
    if not resume or resume.filename == "":
        return render_template(
            "upload.html",
            error="Please select a resume file."
        )

    print("Filename:", resume.filename)

    # Secure filename
    filename = secure_filename(resume.filename)

    # Currently support PDF
    if not filename.lower().endswith(".pdf"):
        return render_template(
            "upload.html",
            error="Please upload your resume in PDF format."
        )

    # Ensure uploads folder exists
    os.makedirs("uploads", exist_ok=True)

    # Save file
    filepath = os.path.join("uploads", filename)

    resume.save(filepath)

    print("Resume saved successfully")
    print("Saved path:", filepath)

    # Check file exists
    if not os.path.exists(filepath):
        return render_template(
            "upload.html",
            error="The resume could not be saved. Please try again."
        )

    # Check file size
    if os.path.getsize(filepath) == 0:
        return render_template(
            "upload.html",
            error="The uploaded PDF is empty. Please upload another PDF."
        )

    # Validate PDF header
    with open(filepath, "rb") as f:
        pdf_header = f.read(5)

    if pdf_header != b"%PDF-":
        return render_template(
            "upload.html",
            error=(
                "The uploaded file is not a valid PDF. "
                "Please open your resume and save it again as PDF."
            )
        )

    print("Valid PDF detected")

    # =========================
    # RESUME ANALYSIS
    # =========================

    analysis = analyze_resume(filepath)

    print("Resume analysis completed")

    resume_text = analysis.get("text", "")
    detected_skills = analysis.get("skills", [])
    categorized = analysis.get("categorized", {})
    missing = analysis.get("missing", [])
    ats_score = analysis.get("ats_score", 0)
    suggestions = analysis.get("suggestions", [])
    career_advice = analysis.get("career", [])
    predicted_roles = analysis.get("roles", [])
    section_report = analysis.get("sections", {})
    resume_strength = analysis.get("strength", {})

    # =========================
    # JOB DESCRIPTION
    # =========================

    job_description = request.form.get(
        "job_description",
        ""
    ).strip()

    # =========================
    # JOB MATCH
    # =========================

    job_match = calculate_job_match(
        resume_text,
        job_description
    )

    print("Job matching completed")

    # =========================
    # AI RESUME REVIEW
    # =========================

    ai_review = ask_resume_ai(
        f"""
You are an ATS Resume Expert.

Analyze the following resume.

Give your response in this format:

1. Overall Resume Review
2. Strengths
3. Weaknesses
4. ATS Improvement Suggestions
5. Career Advice

Resume:

{resume_text}
"""
    )

    print("AI resume review completed")

    # =========================
    # INTERVIEW QUESTIONS
    # =========================

    interview_questions = generate_interview_questions(
        resume_text
    )

    # =========================
    # COVER LETTER
    # =========================

    cover_letter = generate_cover_letter(
        resume_text
    )

    # =========================
    # RESUME REWRITE
    # =========================

    rewritten_resume = rewrite_resume(
        resume_text
    )

    # =========================
    # CAREER ROADMAP
    # =========================

    roadmap = generate_roadmap(
        detected_skills
    )

    # =========================
    # CAREER ADVICE
    # =========================

    career_advice_text = "\n".join(
        career_advice
    ) if isinstance(career_advice, list) else str(
        career_advice
    )

    # =========================
    # RESUME RATING
    # =========================

    resume_rating = resume_strength.get(
        "score",
        0
    )

    resume_level = resume_strength.get(
        "level",
        "Beginner"
    )

    # Chat is now handled exclusively on the /analysis page via
    # /resume-chat, so no chat happens during upload itself.
    chat_answer = ""

    # =========================
    # SAVE TO DATABASE
    # (resume_text / roadmap / career_advice / chat_answer live
    #  here, server-side, NOT in the session cookie)
    # =========================

    conn = sqlite3.connect("resumeiq.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO resume_history
        (
            user_id,
            filename,
            ats_score,
            skills_count,
            job_matches,
            resume_rating,
            resume_text,
            roadmap,
            career_advice,
            chat_answer
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            session["user_id"],
            filename,
            ats_score,
            len(detected_skills),
            job_match,
            resume_level,
            resume_text,
            roadmap,
            career_advice_text,
            chat_answer
        )
    )

    conn.commit()

    resume_id = cursor.lastrowid

    conn.close()

    print("Resume history saved")
    print("New resume_id:", resume_id)

    # =========================
    # SAVE SESSION DATA
    # Only small values go into the session cookie.
    # =========================

    session["resume_id"] = resume_id
    session["ats_score"] = ats_score
    session["skills_count"] = len(detected_skills)
    session["detected_skills"] = detected_skills
    session["job_matches"] = job_match
    session["resume_rating"] = resume_rating

    # =========================
    # GENERATE PDF REPORT
    # =========================

    pdf_path = os.path.join(
        "uploads",
        "ResumeIQ_Report.pdf"
    )

    generate_pdf(
        pdf_path,
        ats_score,
        detected_skills,
        missing,
        ai_review
    )

    print("PDF report generated")

    # =========================
    # DISPLAY RESULTS
    # (passed directly to the template for THIS request only —
    #  none of this large content is stored in the session)
    # =========================

    return render_template(
        "upload.html",

        extracted_text=resume_text,

        detected_skills=detected_skills,

        categorized=categorized,

        missing=missing,

        ats_score=ats_score,

        suggestions=suggestions,

        career_advice=career_advice,

        predicted_roles=predicted_roles,

        section_report=section_report,

        resume_strength=resume_strength,

        ai_review=ai_review,

        interview_questions=interview_questions,

        job_match=job_match,

        cover_letter=cover_letter,

        rewritten_resume=rewritten_resume,

        roadmap=roadmap,

        chat_answer=chat_answer,

        pdf_file=pdf_path
    )


@app.route("/download-report")
def download_report():
    if "user_id" not in session:
        return redirect(url_for("login"))

    return send_file(
        "uploads/ResumeIQ_Report.pdf",
        as_attachment=True
    )


@app.route("/history")
def history():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("resumeiq.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT filename,
               ats_score,
               upload_date
        FROM resume_history
        WHERE user_id=?
        ORDER BY upload_date DESC
        """,
        (session["user_id"],)
    )

    resumes = cursor.fetchall()
    conn.close()

    return render_template(
        "history.html",
        resumes=resumes,
        username=session.get("user_name")
    )


@app.route("/clear-history", methods=["POST"])
def clear_history():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("resumeiq.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM resume_history WHERE user_id=?",
        (session["user_id"],)
    )

    conn.commit()
    conn.close()

    # The resume the user was looking at no longer exists.
    session.pop("resume_id", None)

    return redirect(url_for("history"))


@app.route("/send-report", methods=["POST"])
def send_report_route():
    if "user_id" not in session:
        return redirect(url_for("login"))

    receiver = request.form.get("email")
    report = request.form.get("report")

    send_report(receiver, report)

    return {
        "status": "success"
    }


@app.route("/analysis")
def analysis():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    resume_id = session.get("resume_id")

    resume_row = None

    if resume_id:
        resume_row = get_resume_by_id(resume_id, user_id)

    # Fallback: if session resume_id is missing/stale, use the
    # user's most recent resume instead.
    if not resume_row:
        resume_row = get_latest_resume(user_id)

    if resume_row:
        ats_score = resume_row["ats_score"] or 0
        skills_count = resume_row["skills_count"] or 0
        job_matches = resume_row["job_matches"] or 0
        resume_rating = resume_row["resume_rating"] or "N/A"
        resume_text = resume_row["resume_text"] or ""
        chat_answer = resume_row["chat_answer"] or ""
    else:
        ats_score = 0
        skills_count = 0
        job_matches = 0
        resume_rating = "N/A"
        resume_text = ""
        chat_answer = ""

    return render_template(
        "analysis.html",
        username=session["user_name"],
        ats_score=ats_score,
        skills_count=skills_count,
        job_matches=job_matches,
        resume_rating=resume_rating,
        detected_skills=session.get("detected_skills", []),
        resume_text=resume_text,
        chat_answer=chat_answer
    )


@app.route("/resume-chat", methods=["POST"])
def resume_chat():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    resume_id = session.get("resume_id")

    user_question = request.form.get("user_question", "").strip()

    print("================================")
    print("RESUME CHAT DEBUG")
    print("User ID:", user_id)
    print("Resume ID:", resume_id)
    print("Question:", user_question)

    if not user_question:
        if resume_id:
            update_chat_answer(
                resume_id,
                user_id,
                "Please enter a question."
            )
        print("================================")
        return redirect(url_for("analysis"))

    if not resume_id:
        print("No resume_id found in session.")
        print("================================")
        return redirect(url_for("analysis"))

    # SECURITY: fetch by id AND user_id together, so one user can
    # never load another user's resume by guessing an id.
    resume_row = get_resume_by_id(resume_id, user_id)

    if not resume_row:
        print("Resume not found for this user.")
        print("================================")
        return redirect(url_for("analysis"))

    resume_text = resume_row["resume_text"] or ""

    print("Resume length:", len(resume_text))
    print("Resume exists:", bool(resume_text))

    if not resume_text:
        update_chat_answer(
            resume_id,
            user_id,
            "No resume is currently loaded. Please upload your resume again."
        )
        print("================================")
        return redirect(url_for("analysis"))

    try:
        chat_answer = chat_with_resume(resume_text, user_question)
        print("AI answer length:", len(chat_answer))

    except Exception as e:
        print("Resume chat failed:", repr(e))
        chat_answer = (
            "AI service temporarily unavailable. "
            "Please try again."
        )

    update_chat_answer(resume_id, user_id, chat_answer)

    print("================================")

    return redirect(url_for("analysis"))


@app.route("/career")
def career():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    resume_id = session.get("resume_id")

    resume_row = None

    if resume_id:
        resume_row = get_resume_by_id(resume_id, user_id)

    if not resume_row:
        resume_row = get_latest_resume(user_id)

    roadmap = resume_row["roadmap"] if resume_row else ""
    career_advice = resume_row["career_advice"] if resume_row else ""

    return render_template(
        "career.html",
        username=session["user_name"],
        roadmap=roadmap or "",
        career_advice=career_advice or ""
    )


@app.route("/reports")
def reports():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "reports.html",
        username=session.get("user_name", "User"),
        ats_score=session.get("ats_score", 0),
        skills_count=session.get("skills_count", 0),
        job_matches=session.get("job_matches", 0),
        resume_rating=session.get("resume_rating", 0)
    )


@app.route("/settings")
def settings():
    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "settings.html",
        username=session["user_name"]
    )


@app.route("/debug-session")
def debug_session():

    if "user_id" not in session:
        return "Not logged in"

    user_id = session["user_id"]
    resume_id = session.get("resume_id")

    resume_row = get_resume_by_id(resume_id, user_id) if resume_id else None

    resume_text = resume_row["resume_text"] if resume_row else ""
    chat_answer = resume_row["chat_answer"] if resume_row else ""

    return {
        "session_keys": list(session.keys()),
        "resume_id": resume_id,
        "resume_loaded": bool(resume_text),
        "resume_length": len(resume_text or ""),
        "chat_answer": chat_answer or ""
    }


if __name__ == "__main__":
    app.run(
        debug=True,
        use_reloader=False
    )