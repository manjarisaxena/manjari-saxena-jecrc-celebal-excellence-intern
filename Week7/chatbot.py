"""
chatbot.py
----------
Handles grounded answer generation using Cohere's Chat API in RAG mode.
Cohere's Command models natively support a `documents` parameter and return
fine-grained inline citations pointing back to exactly which retrieved chunk
supported each part of the answer.
"""

import cohere


class DocSenseChatbot:
    def __init__(self, cohere_api_key: str, model: str = "command-r-plus-08-2024"):
        self.co = cohere.Client(cohere_api_key)
        self.model = model

    def answer(self, question: str, retrieved_chunks: list[dict], chat_history: list[dict] = None) -> dict:
        """
        Generate a grounded answer using retrieved chunks as RAG context.

        retrieved_chunks: list of {"id", "text", "source", "chunk_id", "score"}
        chat_history: list of {"role": "USER"/"CHATBOT", "message": str}
        """
        documents = [
            {
                "id": chunk["id"],
                "title": f'{chunk["source"]} — chunk {chunk["chunk_id"]}',
                "text": chunk["text"],
            }
            for chunk in retrieved_chunks
        ]

        response = self.co.chat(
            message=question,
            model=self.model,
            documents=documents,
            chat_history=chat_history or [],
            temperature=0.3,
        )

        citations = []
        if response.citations:
            for c in response.citations:
                citations.append({
                    "text": c.text,
                    "start": c.start,
                    "end": c.end,
                    "document_ids": getattr(c, "document_ids", []),
                })

        return {
            "answer": response.text,
            "citations": citations,
            "retrieved_chunks": retrieved_chunks,
        }
