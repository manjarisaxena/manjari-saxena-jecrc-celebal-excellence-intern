"""
app.py
------
ScrollMind AI — a RAG-based Document Question Answering chatbot.
Cohere (embeddings + grounded generation) + Pinecone (vector search) + Streamlit (UI).
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

import streamlit as st
from knowledge_base import KnowledgeBase, extract_text_from_pdf, chunk_text
from response_engine import ResponseEngine

st.set_page_config(page_title="ScrollMind AI", page_icon="📜", layout="wide")

# ---------------------------------------------------------------------------
# DARK THEME
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background-color: #071019;
        color: #dcecec;
    }
    section[data-testid="stSidebar"] {
        background-color: #0b1721;
        border-right: 1px solid #1a3540;
    }
    section[data-testid="stSidebar"] * {
        color: #dcecec !important;
    }
    /* Field labels (Cohere API Key, Upload Documents, etc.) */
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown p,
    label, .stMarkdown p {
        color: #dcecec !important;
    }
    /* Captions / help text (greyed out too much by default) */
    .stCaption, [data-testid="stCaptionContainer"], small {
        color: #8fb4bd !important;
    }
    /* Text input boxes */
    input, textarea {
        background-color: #0f2530 !important;
        color: #eafbfb !important;
        caret-color: #eafbfb !important;
    }
    input::placeholder, textarea::placeholder {
        color: #6c8f99 !important;
        opacity: 1;
    }
    /* File uploader drag-and-drop box */
    section[data-testid="stFileUploaderDropzone"] {
        background-color: #0f2530 !important;
        border: 1px dashed #1f4552 !important;
    }
    section[data-testid="stFileUploaderDropzone"] * {
        color: #dcecec !important;
    }
    /* Buttons */
    button {
        color: #eafbfb !important;
    }
    .stChatMessage {
        background-color: #0f2530;
        border-radius: 12px;
        border: 1px solid #1a3540;
        color: #eafbfb !important;
    }
    .stChatMessage * {
        color: #eafbfb !important;
    }
    .doc-badge {
        display: inline-block;
        background: linear-gradient(135deg, #0891b2, #06b6d4);
        color: white !important;
        padding: 2px 10px;
        border-radius: 999px;
        font-size: 0.75rem;
        margin-right: 6px;
    }
    .citation-tag {
        background-color: #123842;
        color: #5eead4 !important;
        border-radius: 6px;
        padding: 1px 6px;
        font-size: 0.75rem;
        margin-left: 4px;
    }
    .stat-card {
        background-color: #0f2530;
        border: 1px solid #1a3540;
        border-radius: 10px;
        padding: 10px 14px;
        margin-bottom: 8px;
        color: #eafbfb !important;
    }
    .stat-card * { color: #eafbfb !important; }
    h1, h2, h3, h4 { color: #eafbfb !important; }
    /* Chat input box at the bottom */
    [data-testid="stChatInput"] textarea {
        background-color: #0f2530 !important;
        color: #eafbfb !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------------------------
if "store" not in st.session_state:
    st.session_state.store = None
if "chatbot" not in st.session_state:
    st.session_state.chatbot = None
if "messages" not in st.session_state:
    st.session_state.messages = []  # [{"role", "content", "citations"?, "sources"?}]
if "doc_stats" not in st.session_state:
    st.session_state.doc_stats = []
if "chat_history_raw" not in st.session_state:
    st.session_state.chat_history_raw = []  # cohere-format history for context

# ---------------------------------------------------------------------------
# SIDEBAR — API KEYS + DOCUMENT UPLOAD
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 📜 ScrollMind AI")
    st.caption("Read deep, ask smart — Cohere + Pinecone powered document Q&A")

    st.markdown("### 🔑 API Keys")
    cohere_key = st.text_input("Cohere API Key", type="password", help="https://dashboard.cohere.com/api-keys")
    pinecone_key = st.text_input("Pinecone API Key", type="password", help="https://app.pinecone.io")

    keys_ready = bool(cohere_key and pinecone_key)
    if not keys_ready:
        st.info("Enter both API keys to get started.")

    st.markdown("### 📄 Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload one or more PDFs", type=["pdf"], accept_multiple_files=True, disabled=not keys_ready
    )

    top_k = st.slider("Chunks to retrieve per question", min_value=2, max_value=8, value=4)

    if uploaded_files and keys_ready:
        if st.button("⚙️ Process Documents", use_container_width=True):
            with st.spinner("Extracting, chunking, and embedding your documents..."):
                if st.session_state.store is None:
                    st.session_state.store = KnowledgeBase(cohere_key, pinecone_key)
                    st.session_state.chatbot = ResponseEngine(cohere_key)

                for f in uploaded_files:
                    already_done = any(s["source"] == f.name for s in st.session_state.doc_stats)
                    if already_done:
                        continue
                    text = extract_text_from_pdf(f.read())
                    chunks = chunk_text(text)
                    stats = st.session_state.store.add_document(chunks, source_name=f.name)
                    st.session_state.doc_stats.append(stats)
            st.success(f"Processed {len(uploaded_files)} document(s) ✅")

    if st.session_state.doc_stats:
        st.markdown("### 📊 Indexed Documents")
        for s in st.session_state.doc_stats:
            st.markdown(f"""
            <div class="stat-card">
                <span class="doc-badge">{s['num_chunks']} chunks</span>
                <b>{s['source']}</b><br>
                <small>Embedding: {s['embedding_model']} ({s['embedding_dim']}-dim) · {s['ingestion_time_sec']}s</small>
            </div>
            """, unsafe_allow_html=True)

    if st.session_state.messages:
        chat_txt = "\n\n".join(
            f"{'You' if m['role']=='user' else 'ScrollMind AI'}: {m['content']}"
            for m in st.session_state.messages
        )
        st.download_button("⬇️ Download chat history", chat_txt, file_name="scrollmind_chat_history.txt",
                            use_container_width=True)

# ---------------------------------------------------------------------------
# MAIN — CHAT INTERFACE
# ---------------------------------------------------------------------------
st.title("📜 ScrollMind AI")
st.caption("Ask questions grounded in your own documents — answers cite exactly which chunk they came from.")

if not keys_ready:
    st.warning("👈 Add your Cohere and Pinecone API keys in the sidebar to begin.")
elif not st.session_state.doc_stats:
    st.info("👈 Upload and process at least one PDF to start chatting.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("📚 View retrieved sources"):
                for src in msg["sources"]:
                    st.markdown(
                        f"**{src['source']}** — chunk {src['chunk_id']} "
                        f"<span class='citation-tag'>score: {src['score']:.3f}</span>",
                        unsafe_allow_html=True,
                    )
                    st.caption(src["text"][:300] + "...")

question = st.chat_input("Ask something about your documents...", disabled=not st.session_state.doc_stats)

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Retrieving context and generating answer..."):
            retrieved = st.session_state.store.search(question, top_k=top_k)
            result = st.session_state.chatbot.answer(
                question, retrieved, chat_history=st.session_state.chat_history_raw
            )
            st.markdown(result["answer"])

            if result["citations"]:
                with st.expander(f"📚 View retrieved sources ({len(result['citations'])} citations found)"):
                    for src in retrieved:
                        st.markdown(
                            f"**{src['source']}** — chunk {src['chunk_id']} "
                            f"<span class='citation-tag'>score: {src['score']:.3f}</span>",
                            unsafe_allow_html=True,
                        )
                        st.caption(src["text"][:300] + "...")
            else:
                with st.expander("📚 View retrieved sources"):
                    for src in retrieved:
                        st.markdown(f"**{src['source']}** — chunk {src['chunk_id']} (score: {src['score']:.3f})")
                        st.caption(src["text"][:300] + "...")

    st.session_state.messages.append({
        "role": "assistant", "content": result["answer"], "sources": retrieved,
    })
    st.session_state.chat_history_raw.append({"role": "USER", "message": question})
    st.session_state.chat_history_raw.append({"role": "CHATBOT", "message": result["answer"]})
