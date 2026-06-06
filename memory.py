import mysql.connector
import streamlit as st

# -------------------------
# DB CONNECTION
# -------------------------
def get_conn():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_PASSWORD",
        database="ai_agent"
    )

# -------------------------
# INIT USER SESSION
# -------------------------
def initialize_memory():
    if "user_id" not in st.session_state:
        st.session_state.user_id = None

    if "username" not in st.session_state:
        st.session_state.username = None

# -------------------------
# LOGIN / CREATE USER
# -------------------------
def login_user(username):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()

    if user:
        user_id = user[0]
    else:
        cursor.execute(
            "INSERT INTO users (username) VALUES (%s)",
            (username,)
        )
        conn.commit()
        user_id = cursor.lastrowid

    conn.close()

    st.session_state.user_id = user_id
    st.session_state.username = username

# -------------------------
# ADD MESSAGE
# -------------------------
def add_message(role, content):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO messages (user_id, role, content) VALUES (%s, %s, %s)",
        (st.session_state.user_id, role, content)
    )

    conn.commit()
    conn.close()

# -------------------------
# GET HISTORY (USER-SPECIFIC)
# -------------------------
def get_history():
    if not st.session_state.user_id:
        return []

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT role, content FROM messages WHERE user_id=%s ORDER BY timestamp",
        (st.session_state.user_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    return [{"role": r[0], "content": r[1]} for r in rows]

# -------------------------
# GET ALL CHATS (optional sidebar history)
# -------------------------
def get_chat_sessions():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT u.username, u.id
        FROM users u
        ORDER BY u.id DESC
    """)

    data = cursor.fetchall()
    conn.close()

    return data
