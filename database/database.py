import sqlite3

DATABASE = "resumeiq.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        fullname TEXT,

        email TEXT UNIQUE,

        password TEXT

    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resume_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        filename TEXT,

        ats_score INTEGER,

        skills_count INTEGER,

        job_matches INTEGER,

        resume_rating TEXT,

        upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()

    # =========================================================
    # SAFE MIGRATION
    # CREATE TABLE IF NOT EXISTS will NOT add columns to an
    # existing table, so we check PRAGMA table_info and add
    # any missing columns without touching existing data.
    # =========================================================

    cursor.execute("PRAGMA table_info(resume_history)")
    existing_columns = [row[1] for row in cursor.fetchall()]

    required_columns = {
        "resume_text": "TEXT",
        "roadmap": "TEXT",
        "career_advice": "TEXT",
        "chat_answer": "TEXT",
    }

    for column_name, column_type in required_columns.items():
        if column_name not in existing_columns:
            cursor.execute(
                f"ALTER TABLE resume_history ADD COLUMN {column_name} {column_type}"
            )
            print(f"[DB MIGRATION] Added missing column '{column_name}' to resume_history")

    conn.commit()
    conn.close()


# =============================================================
# HELPER FUNCTIONS
# Centralizing these keeps app.py simple and avoids duplicated
# SQL scattered across routes.
# =============================================================

def get_resume_by_id(resume_id, user_id):
    """
    Fetch a single resume_history row, but ONLY if it belongs
    to the given user_id. This prevents one user from reading
    another user's resume via a guessed/stale resume_id.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM resume_history
        WHERE id = ? AND user_id = ?
        """,
        (resume_id, user_id)
    )

    row = cursor.fetchone()
    conn.close()
    return row


def get_latest_resume(user_id):
    """
    Fallback: fetch the most recently uploaded resume for a user,
    used when session['resume_id'] is missing or stale.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM resume_history
        WHERE user_id = ?
        ORDER BY upload_date DESC
        LIMIT 1
        """,
        (user_id,)
    )

    row = cursor.fetchone()
    conn.close()
    return row


def update_chat_answer(resume_id, user_id, chat_answer):
    """
    Store the latest AI chat answer server-side (in the database)
    instead of in the Flask session cookie.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE resume_history
        SET chat_answer = ?
        WHERE id = ? AND user_id = ?
        """,
        (chat_answer, resume_id, user_id)
    )

    conn.commit()
    conn.close()