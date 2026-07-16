import io
import re
from pypdf import PdfReader
import docx2txt

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
        # Find all words/tokens (including +, #, etc.) using regex
        tokens = re.findall(r'[a-zA-Z0-9+#.-]+', text.lower())
        # Strip trailing punctuation (like trailing periods or commas)
        cleaned_tokens = {token.strip('.,-') for token in tokens}
        # Intersection with skill library
        found_skills = cleaned_tokens.intersection(skill_library)
        return sorted(found_skills)
