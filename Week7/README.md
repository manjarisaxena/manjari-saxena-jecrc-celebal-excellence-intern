# ScrollMind AI 📜🌊
### RAG-Based Document Question Answering System

A Retrieval-Augmented Generation chatbot that lets you upload PDFs and ask
questions grounded in their content — with **native inline citations** showing
exactly which chunk of your document backs each part of the answer.

Built with **Cohere** (embeddings + grounded generation), **Pinecone**
(vector search), and **Streamlit** (UI).

---

## What makes this different ✨

- **Grounded answers with real citations** — uses Cohere's Chat API `documents`
  parameter, which returns fine-grained inline citations pointing to the exact
  retrieved chunk that supports each claim (not just "trust me, I read it").
- **Multi-document support** — upload several PDFs at once; each gets its own
  metadata tag so you always know which source an answer came from.
- **Session-scoped Pinecone namespace** — every session gets its own namespace,
  so your queries never accidentally mix with someone else's documents on the
  same index.
- **Transparent retrieval** — every answer comes with an expandable "View
  retrieved sources" panel showing the actual chunks + similarity scores used.
- **Dark, distraction-free UI** — built for actually reading long answers
  without eye strain.
- **Downloadable chat history** — export your Q&A session as a `.txt` file.

---

## Architecture

```
PDF Upload (Streamlit)
        │
        ▼
Text Extraction (PyMuPDF)
        │
        ▼
Chunking (overlapping word-based chunks)
        │
        ▼
Embedding (Cohere embed-english-v3.0, 1024-dim)
        │
        ▼
Vector Storage (Pinecone serverless index, per-session namespace)
        │
   [User Question]
        │
        ▼
Query Embedding → Pinecone similarity search (top-k)
        │
        ▼
Grounded Generation (Cohere command-r-plus, with `documents=` param)
        │
        ▼
Answer + Inline Citations + Source Chunks (Streamlit chat UI)
```

---

## Project Structure 📁
```
scrollmind_rag/
├── src/
│   ├── ui_app.py          # Streamlit UI — chat interface, upload, dark theme
│   ├── knowledge_base.py  # PDF extraction, chunking, Cohere embeddings, Pinecone
│   └── response_engine.py # Grounded generation via Cohere Chat API + citations
├── requirements.txt
├── LICENSE
└── README.md
```

---

## How to Use 🚀

### 1. Clone / open the project
```bash
cd scrollmind_rag
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Get your API keys 🔑
- **Cohere** — sign up free at https://dashboard.cohere.com/api-keys
- **Pinecone** — sign up free at https://app.pinecone.io

Both keys are entered directly in the Streamlit sidebar when you run the app —
no `.env` file needed.

### 5. Run the app
```bash
cd src
streamlit run ui_app.py
```

### 6. Use it
1. Paste your Cohere and Pinecone API keys in the sidebar.
2. Upload one or more PDFs and click **"Process Documents"**.
3. Ask questions in the chat box.
4. Expand **"View retrieved sources"** under any answer to see exactly which
   chunks were used, with similarity scores.

---

## Configuration Notes

- **Embedding model:** `embed-english-v3.0` (1024-dim), with `input_type` set
  correctly for documents (`search_document`) vs. queries (`search_query`) —
  this matters a lot for Cohere's retrieval quality.
- **Vector index:** Pinecone serverless (AWS, `us-east-1`), cosine similarity.
  Each app session gets an isolated namespace so documents from different
  sessions never mix.
- **Generation model:** `command-r-plus-08-2024`, Cohere's model purpose-built
  for RAG — it's trained specifically to cite the documents you give it rather
  than relying on parametric memory.
- **Chunking:** word-based with overlap (default 300 words / 50-word overlap),
  tunable in `vectorstore.chunk_text()`.

## Future Enhancements 🚧
- Add Cohere Rerank as a second-stage filter before generation.
- Hybrid search (BM25 + vector) for better exact-keyword recall.
- Multi-turn follow-up question handling using `chat_history`.
- Persist Pinecone namespace per document set instead of per session, so
  users can return to previously uploaded documents.
- Deploy to Streamlit Community Cloud for shareable public access.

---

## License 📜
Licensed under the Apache License 2.0. See `LICENSE` for details.

## Acknowledgments 🙏
- **Cohere** for embeddings and grounded generation with built-in citations.
- **Pinecone** for scalable serverless vector search.
- **Streamlit** for making the interface effortless to build.
