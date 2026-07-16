from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQA

from app.config import settings


class ExplainableAIEngine:
    def __init__(self):
        if settings.GOOGLE_API_KEY:
            self.embeddings = GoogleGenerativeAIEmbeddings(
               model="models/gemini-embedding-001", google_api_key=settings.GOOGLE_API_KEY
            )
            self.llm = ChatGoogleGenerativeAI(
            model="gemini-flash-latest", google_api_key=settings.GOOGLE_API_KEY, temperature=0.2,
            convert_system_message_to_human=True
            )
        else:
            self.embeddings = None
            self.llm = None

    def generate_rag_feedback(self, resume_text: str, missing_skills: list) -> str:
        if not missing_skills:
            return "Great match — no missing skills detected against this job description."

        if not self.llm:
            return (
                f"Missing skills: {', '.join(missing_skills)}. "
                "Set GOOGLE_API_KEY in the backend .env file to get personalized AI feedback."
            )

        docs = [Document(page_content=resume_text, metadata={"source": "resume"})]
        vectorstore = FAISS.from_documents(docs, self.embeddings)
        query = (
            "Compare this candidate's background against these missing skills: "
            f"{', '.join(missing_skills)}. Give 3-4 short, actionable learning steps."
        )
        qa_chain = RetrievalQA.from_chain_type(llm=self.llm, retriever=vectorstore.as_retriever())
        return qa_chain.run(query)
