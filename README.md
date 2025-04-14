# 🕶️ SHADOW: Secure Intelligence Assistant (RAG + Rules + Graph)

SHADOW is a classified AI simulation assistant designed to emulate agent-level query response logic using Retrieval-Augmented Generation (RAG), graph traversal, and rule-based systems.

---

## 🔧 Project Structure

```
shadow/
├── app/
│   ├── agent_levels.py          # Greeting & role logic per agent level
│   ├── database.py              # SQLModel-based SQLite DB
│   ├── models.py                # Chat and ChatMessage tables
│   ├── query_parser.py          # Basic query processing
│   ├── rule_engine.py           # Optional fixed rule logic
│   ├── rag_indexer.py           # Builds FAISS index from PDF
│   ├── rag_searcher.py          # Vector-based semantic retrieval
│   ├── pdf_ingestor.py          # Splits and extracts PDFs into chunks
│   └── knowledge_base/
│       ├── SECRET INFO MANUAL.pdf
│       ├── RAG CASE RESPONSE FRAMEWORK.pdf
│       ├── rag_index.faiss
│       └── rag_metadata.json
│
├── web/
│   ├── main_fastapi.py          # FastAPI application
│   └── templates/
│       └── chat.html            # GPT-style chat UI with sidebar
│
├── tests/
│   └── test_rag.py              # Test RAG retrieval
├── logs/
│   └── queries.log              # Logged user queries
└── README.md                    # This file
```

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/shadow
cd shadow
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/Scripts/activate  # On Windows
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

> You may also need:
```bash
pip install faiss-cpu pymupdf sentence-transformers sqlmodel
```

---

## 🚀 Usage

### 🧠 Build the Knowledge Base Index

```bash
python app/rag_indexer.py
```

This will:
- Parse both PDFs
- Chunk them
- Create `rag_index.faiss` + `rag_metadata.json`

---

### 🔗 Run the FastAPI Chat App

```bash
uvicorn web.main_fastapi:app --reload
```

Visit [http://localhost:8000](http://localhost:8000)

- Login as: `shadow1 / agent001`
- Query with any classified intel
- View secure responses, based on agent level

---

## 🔍 Features

- 🔐 Login system with agent-level roles (1–5)
- 💬 ChatGPT-style assistant with multi-chat sidebar
- 🧠 Semantic RAG-based retrieval
- 🔒 Security clearance enforcement on sensitive content
- ✏️ Rename, ❌ Delete, 🔎 Search chats
- 📄 PDF parsing + embedding pipeline

---

## 📤 Future Ideas

- Export chat as JSON / PDF  
- Integrate GPT for natural summaries  
- Add graph-based rule inference (via NetworkX or Neo4j)  
- Admin dashboard for flagged queries  

---

## 🛡️ License

This project simulates a fictional intelligence assistant. Not affiliated with any real agency.

MIT License.