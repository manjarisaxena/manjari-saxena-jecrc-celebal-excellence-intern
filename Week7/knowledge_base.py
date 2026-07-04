"""
vectorstore.py
--------------
Handles PDF ingestion, text chunking, Cohere embeddings, and Pinecone
vector storage + retrieval for the ScrollMind AI RAG system.
"""

import uuid
import time
import fitz  # PyMuPDF
import cohere
from pinecone import Pinecone, ServerlessSpec


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract raw text from an in-memory PDF file (Streamlit uploaded file)."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = "\n".join(page.get_text() for page in doc)
    doc.close()
    return text


def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    """Split text into overlapping word-based chunks."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        if chunk.strip():
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


class KnowledgeBase:
    """
    Wraps Cohere (embeddings) + Pinecone (vector storage/search) into a single
    interface used by the Streamlit app.
    """

    EMBED_MODEL = "embed-english-v3.0"   # 1024-dim
    EMBED_DIM = 1024

    def __init__(self, cohere_api_key: str, pinecone_api_key: str, index_name: str = "scrollmind-rag"):
        self.co = cohere.Client(cohere_api_key)
        self.pc = Pinecone(api_key=pinecone_api_key)
        self.index_name = index_name
        self._ensure_index()
        self.index = self.pc.Index(self.index_name)
        # A fresh namespace per session/document keeps queries scoped to just
        # the document(s) uploaded in this session, instead of mixing results
        # across every document ever indexed on this Pinecone index.
        self.namespace = f"session-{uuid.uuid4().hex[:12]}"
        self.chunk_lookup: dict[str, dict] = {}   # id -> {"text":, "source":, "chunk_id":}

    def _ensure_index(self):
        existing = [idx["name"] for idx in self.pc.list_indexes()]
        if self.index_name not in existing:
            self.pc.create_index(
                name=self.index_name,
                dimension=self.EMBED_DIM,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
            # Wait for the index to be ready
            while not self.pc.describe_index(self.index_name).status["ready"]:
                time.sleep(1)

    def add_document(self, chunks: list[str], source_name: str, batch_size: int = 90) -> dict:
        """Embed chunks with Cohere and upsert them into Pinecone."""
        t0 = time.time()
        vectors = []
        for i, chunk in enumerate(chunks):
            vec_id = f"{source_name}-{i}-{uuid.uuid4().hex[:6]}"
            self.chunk_lookup[vec_id] = {"text": chunk, "source": source_name, "chunk_id": i}
            vectors.append(vec_id)

        embeddings = []
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            resp = self.co.embed(texts=batch, model=self.EMBED_MODEL, input_type="search_document")
            embeddings.extend(resp.embeddings)

        upserts = [
            (vec_id, embedding, {"source": source_name, "chunk_id": idx, "text": chunk[:1000]})
            for vec_id, embedding, idx, chunk in zip(vectors, embeddings, range(len(chunks)), chunks)
        ]

        for i in range(0, len(upserts), batch_size):
            self.index.upsert(vectors=upserts[i:i + batch_size], namespace=self.namespace)

        return {
            "source": source_name,
            "num_chunks": len(chunks),
            "embedding_model": self.EMBED_MODEL,
            "embedding_dim": self.EMBED_DIM,
            "ingestion_time_sec": round(time.time() - t0, 2),
        }

    def search(self, query: str, top_k: int = 4) -> list[dict]:
        """Embed the query and retrieve the most similar chunks from Pinecone."""
        q_emb = self.co.embed(texts=[query], model=self.EMBED_MODEL, input_type="search_query").embeddings[0]
        results = self.index.query(
            vector=q_emb,
            top_k=top_k,
            include_metadata=True,
            namespace=self.namespace,
        )
        return [
            {
                "id": match["id"],
                "score": match["score"],
                "text": match["metadata"]["text"],
                "source": match["metadata"]["source"],
                "chunk_id": match["metadata"]["chunk_id"],
            }
            for match in results["matches"]
        ]
