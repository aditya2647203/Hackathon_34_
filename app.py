import os
import streamlit as st

import os
import streamlit as st

# RAG Files
from pdf_loader import load_pdf
from vector_store import create_vector_store

# Tools
from web_search import search_web
from rag_tool import retrieve_documents

# Memory
from memory import (
 initialize_memory,
 add_message,
 get_history
)

# Agent
from router import route_query
from graph import generate_response


# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
 page_title="Hackathon AI Agent",
 page_icon="🤖",
 layout="wide"
)

initialize_memory()

st.title("🤖 Intelligent Multi-Mode Conversational AI Agent")

st.sidebar.header("📄 Upload Document")

# -----------------------------
# PDF UPLOAD
# -----------------------------

uploaded_file = st.sidebar.file_uploader(
 "Upload a PDF",
 type=["pdf"]
)

pdf_uploaded = False

if uploaded_file:

 try:

 pdf_uploaded = True

 os.makedirs("uploads", exist_ok=True)

 save_path = os.path.join(
 "uploads",
 uploaded_file.name
 )

 with open(save_path, "wb") as f:
 f.write(uploaded_file.read())

 text = load_pdf(save_path)

 create_vector_store(text)

 st.sidebar.success(
 "✅ PDF Indexed Successfully"
 )

 except Exception as e:

 st.sidebar.error(
 f"PDF Processing Error:\n{str(e)}"
 )

# -----------------------------
# DISPLAY CHAT HISTORY
# -----------------------------

for msg in get_history():

 with st.chat_message(msg["role"]):
 st.markdown(msg["content"])

# -----------------------------
# USER INPUT
# -----------------------------

query = st.chat_input(
 "Ask me anything..."
)

if query:

 add_message("user", query)

 with st.chat_message("user"):
 st.markdown(query)

 try:

 mode = route_query(
 query,
 pdf_uploaded
 )

 # ==================================
 # WEB SEARCH MODE
 # ==================================

 if mode == "web":

 try:

 web_results = search_web(query)

 context = "\n".join(
 [
 r.get("body", "")
 for r in web_results
 ]
 )

 prompt = f"""
 Use the search results below to answer.

 Search Results:
 {context}

 Question:
 {query}
 """

 answer = generate_response(prompt)

 answer = (
 "🌐 WEB SEARCH MODE\n\n"
 + answer
 )

 except Exception:

 answer = generate_response(query)

 answer = (
 "⚠️ Web Search Failed\n\n"
 "Using LLM Knowledge Instead\n\n"
 + answer
 )

 # ==================================
 # PDF RAG MODE
 # ==================================

 elif mode == "rag":

 try:

 context = retrieve_documents(query)

 prompt = f"""
 Answer ONLY using the PDF context.

 Context:
 {context}

 Question:
 {query}
 """

 answer = generate_response(prompt)

 answer = (
 "📄 PDF RAG MODE\n\n"
 + answer
 )

 except Exception:

 answer = (
 "❌ Could not retrieve information "
 "from the uploaded PDF."
 )

 # ==================================
 # LLM MODE
 # ==================================

 else:

 answer = generate_response(query)

 answer = (
 "🧠 LLM MODE\n\n"
 + answer
 )

 except Exception as e:

 answer = f"""
❌ SYSTEM ERROR

{str(e)}
"""

 add_message(
 "assistant",
 answer
 )

 with st.chat_message("assistant"):
 st.markdown(answer)
