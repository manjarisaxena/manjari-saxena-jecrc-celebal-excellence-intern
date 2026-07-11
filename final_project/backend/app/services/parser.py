import io

import spacy
from pypdf import PdfReader
import docx2txt

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import os

    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

DEFAULT_SKILL_LIBRARY = [
    "python", "java", "sql", "git", "linux", "react", "fastapi", "mongodb",
    "xgboost", "pytorch", "tensorflow", "aws", "docker", "javascript",
    "typescript", "node", "kubernetes", "gcp", "azure", "nosql",
]


class ResumeParser:
    @staticmethod
    def extract_text(file_bytes: bytes, filename: str) -> str:
        filename = filename.lower()
        if filename.endswith(".pdf"):
            reader = PdfReader(io.BytesIO(file_bytes))
            return " ".join(page.extract_text() or "" for page in reader.pages)
        elif filename.endswith(".docx"):
            return docx2txt.process(io.BytesIO(file_bytes))
        return file_bytes.decode("utf-8", errors="ignore")

    @staticmethod
    def extract_skills(text: str, skill_library: list | None = None) -> list:
        skill_library = skill_library or DEFAULT_SKILL_LIBRARY
        doc = nlp(text.lower())
        found_skills = set()
        for token in doc:
            if token.text in skill_library:
                found_skills.add(token.text)
        return sorted(found_skills)
