from app.memory.db import get_connection


# ── Create new session ────────────────────────────────────────
def create_session():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sessions (title) VALUES (?)", ("New Chat",))
    session_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return session_id


# ── Get all sessions ──────────────────────────────────────────
def get_sessions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ── Get a single session's title ──────────────────────────────
def get_session_title(session_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT title FROM sessions WHERE id=?", (session_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row["title"] if row["title"] != "New Chat" else ""
    return ""


# ── Update session title (called on first message) ────────────
def update_session_title(session_id, title):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE sessions SET title=? WHERE id=?",
        (title, session_id)
    )
    conn.commit()
    conn.close()


# ── Count messages in session (to detect first message) ───────
def get_session_message_count(session_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) as cnt FROM messages WHERE session_id=?",
        (session_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row["cnt"] if row else 0


# ── Add message ───────────────────────────────────────────────
def add_message(session_id, user, bot):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (session_id, user, bot) VALUES (?, ?, ?)",
        (session_id, user, bot)
    )
    conn.commit()
    conn.close()


# ── Get messages of session ───────────────────────────────────
# Returns [{user, bot}] — frontend must transform to [{role, content}]
def get_messages(session_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user, bot FROM messages WHERE session_id=?",
        (session_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ── For query rewrite ─────────────────────────────────────────
def get_chat_list(session_id, limit=5):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user, bot FROM messages WHERE session_id=? ORDER BY id DESC LIMIT ?",
        (session_id, limit)
    )
    rows = cursor.fetchall()
    conn.close()

    chat_history = []
    for row in reversed(rows):
        chat_history.append({
            "user": row["user"],
            "assistant": row["bot"]
        })
    return chat_history


# ── For LLM prompt history ────────────────────────────────────
def get_history(session_id, limit=5):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user, bot FROM messages WHERE session_id=? ORDER BY id DESC LIMIT ?",
        (session_id, limit)
    )
    rows = cursor.fetchall()
    conn.close()

    history = ""
    for row in reversed(rows):
        history += f"User: {row['user']}\n"
        history += f"Assistant: {row['bot']}\n\n"
    return history