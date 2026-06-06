# 🤖 Intelligent Conversational AI Agent

A fully open-source, enterprise-grade conversational AI system capable of answering questions through multiple knowledge sources while maintaining conversational context — built for a hackathon challenge.

---

## 📌 Overview

This agent operates across **three distinct modes**, dynamically selecting the right tool for every query:

| Mode | Description | Tool Invoked |
|------|-------------|--------------|
| 💬 **General Chat** | Answers using LLM internal knowledge | LLM only |
| 🌐 **Web Search** | Retrieves real-time information from the web | DuckDuckGo Search |
| 📄 **RAG Mode** | Answers strictly from ingested enterprise documents | ChromaDB + Embeddings |

---

## 🏗️ Architecture

```
Streamlit UI
    ↕
Agent Orchestrator (LangGraph)
    ↕
┌──────────────┬──────────────┬──────────────┐
│  LLM Tool    │  Web Search  │  RAG Tool    │
│ (Ollama)     │ (DuckDuckGo) │ (ChromaDB)   │
└──────────────┴──────────────┴──────────────┘
    ↕
Memory Store (SQLite)
```

**Stack:**
- **Orchestration:** LangGraph
- **LLM:** Llama 3 8B Instruct via Ollama
- **Embeddings:** `BAAI/bge-small-en-v1.5` (HuggingFace)
- **Vector DB:** ChromaDB (persistent, local)
- **Document Parsing:** pypdf + RecursiveCharacterTextSplitter
- **Memory:** SQLite (`chat_memory.db`)
- **UI:** Streamlit

---

## 📂 Project Structure

```
.
├── memory_utils.py          # Phase 1 — SQLite memory initialization
├── document_processor.py   # Phase 2 — PDF parsing & chunking
├── vector_store.py          # Phase 3 — Embeddings & ChromaDB ingestion
├── retrieval_api.py         # Phase 4 — Retrieval handshake API
├── latency_qa.py            # Phase 5 — Latency benchmarking
├── package_deliverables.py  # Phase 5 — RAG_Documents packaging
├── generate_mock_data.py    # Utility — Mock PDF generator
├── chat_memory.db           # SQLite session memory store
├── chroma_db/               # Persistent ChromaDB vector store (auto-generated)
└── RAG_Documents/           # Packaged evaluation PDFs (auto-generated)
```

---

## 🚀 Quickstart

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai) with Llama 3 8B pulled: `ollama pull llama3`

### 1. Clone & Install

```bash
git clone <repo-url>
cd <repo-name>
pip install -r requirements.txt
```

### 2. Generate Mock Documents (optional)

Populates `E:\Projects\mock_enterprise_docs` with sample enterprise PDFs for testing:

```bash
python generate_mock_data.py
```

### 3. Initialize Memory DB

```bash
python memory_utils.py
```

### 4. Build the Vector Store

Point `MOCK_DOCS_DIR` in `vector_store.py` to your PDF folder, then run:

```bash
python vector_store.py
```

### 5. Test Retrieval

```bash
python retrieval_api.py
```

### 6. Run Latency QA

```bash
python latency_qa.py
```

### 7. Launch the App

```bash
streamlit run app.py
```

---

## 📄 RAG Pipeline

```
PDF Files
  → parse_pdf_with_metadata()     # pypdf page-by-page extraction
  → RecursiveCharacterTextSplitter # chunk_size=1000, overlap=200
  → BAAI/bge-small-en-v1.5        # embedding
  → ChromaDB (collection: enterprise_knowledge)
  → similarity_search(query, k=3)  # sub-second retrieval
```

Each retrieved chunk is formatted as:

```
## Document: <filename>, Page: <page_number>
Content: <chunk text>
```

---

## 🧠 Memory

Session memory is persisted in a local SQLite database (`chat_memory.db`). The agent maintains short-term conversational context across turns within a session, enabling accurate follow-up responses.

---

## ⚡ Performance Targets

| Metric | Target | Status |
|--------|--------|--------|
| Overall response time | < 5 seconds | ✅ |
| Vector retrieval latency | < 1 second | ✅ (verified via `latency_qa.py`) |
| Web search latency | < 3 seconds | ✅ |

Run the benchmark:

```bash
python latency_qa.py
```

---

## 📦 Sample Documents (RAG)

Three mock enterprise PDFs are included for evaluation:

- `HR_Leave_Policy.pdf` — Annual leave, maternity/paternity, sick leave policies
- `Onboarding_Handbook.pdf` — Pre-onboarding checklist, Day 1 orientation schedule
- `Project_Proposal_Alpha.pdf` — Technical architecture for Project Alpha-Flow

---

## 🔑 Key Design Decisions

**Strict RAG grounding** — In RAG mode, the LLM answers *only* from retrieved document chunks. No hallucinations from external knowledge. If context is insufficient, the agent says so explicitly.

**Intelligent tool routing** — The agent uses an intent classifier with rule-based overrides. Keywords like "policy", "handbook", or "contract" trigger RAG; "latest news" or "current" triggers web search; everything else routes to LLM-only.

**No unnecessary tool calls** — The agent invokes exactly one tool path per query. Calling all tools for every query is an explicit anti-pattern here.

**Source attribution** — Every RAG response includes document name, page number, and chunk content so answers are fully traceable.

---

## 🛡️ Constraints

- **Fully open-source stack** — no proprietary or paid APIs
- **Local inference** — LLM runs via Ollama, embeddings via HuggingFace
- **Session isolation** — each user session is independently managed in SQLite

---

## 📋 Requirements

```
langchain-core
langchain-huggingface
langchain-chroma
langchain-text-splitters
pypdf
chromadb
reportlab
streamlit
```

Install all:

```bash
pip install -r requirements.txt
```

---

## 👥 Team

| Member | Role |
|--------|------|
| Aditi Sudheer | Frontend — Streamlit UI, streaming, citations |
| Priya Pratheesh | Backend — Agent orchestrator, intent classifier, tool adapters |
| Aditya Kumar | Infrastructure — Document ingestion, vector DB, SQLite, DevOps |
| Aryan Garg | AI & RAG — Embeddings, LLM, prompts, hallucination prevention |


