import sqlite3
import streamlit as st

DB_PATH = "chat.db"

# -----------------------------
# INIT
# -----------------------------
def initialize_memory():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        role TEXT,
        content TEXT
    )
    """)

    conn.commit()
    conn.close()

    if "user_id" not in st.session_state:
        st.session_state.user_id = None

    if "username" not in st.session_state:
        st.session_state.username = None


# -----------------------------
# LOGIN USER
# -----------------------------
def login_user(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE username=?",
        (username,)
    )
    user = cursor.fetchone()

    if user:
        user_id = user[0]
    else:
        cursor.execute(
            "INSERT INTO users (username) VALUES (?)",
            (username,)
        )
        conn.commit()
        user_id = cursor.lastrowid

    conn.close()

    st.session_state.user_id = user_id
    st.session_state.username = username


# -----------------------------
# ADD MESSAGE
# -----------------------------
def add_message(role, content):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO messages (user_id, role, content)
        VALUES (?, ?, ?)
    """, (st.session_state.user_id, role, content))

    conn.commit()
    conn.close()


# -----------------------------
# GET HISTORY
# -----------------------------
def get_history():
    if not st.session_state.user_id:
        return []

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT role, content
        FROM messages
        WHERE user_id=?
        ORDER BY id ASC
    """, (st.session_state.user_id,))

    rows = cursor.fetchall()
    conn.close()

    return [{"role": r[0], "content": r[1]} for r in rows]
