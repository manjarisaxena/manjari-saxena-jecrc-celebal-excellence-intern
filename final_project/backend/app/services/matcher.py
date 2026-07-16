import os
import math
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from xgboost import XGBClassifier
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config import settings


class HybridScoringEngine:
    def __init__(self):
        if settings.GOOGLE_API_KEY:
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/gemini-embedding-001", google_api_key=settings.GOOGLE_API_KEY
            )
        else:
            self.embeddings = None
        self.model_path = os.path.join("trained_models", "xgb_resume_ranker.json")
        self.xgb_model = self._load_model()

    def _load_model(self):
        if os.path.exists(self.model_path):
            model = XGBClassifier()
            model.load_model(self.model_path)
            return model
        return None

    def compute_semantic_score(self, resume_text: str, jd_text: str) -> float:
        if self.embeddings:
            try:
                # Embed text using Google Gemini Embedding API
                resume_emb = np.array(self.embeddings.embed_query(resume_text)).reshape(1, -1)
                jd_emb = np.array(self.embeddings.embed_query(jd_text)).reshape(1, -1)
                similarity = cosine_similarity(resume_emb, jd_emb)[0][0]
                return float(similarity)
            except Exception as e:
                # Log error and fallback
                print(f"Gemini embedding API failed, falling back to word overlap: {e}")
        
        # Fallback to word overlap Jaccard-like similarity to prevent failures when key is missing/limit reached
        words_resume = set(resume_text.lower().split())
        words_jd = set(jd_text.lower().split())
        if not words_resume or not words_jd:
            return 0.0
        intersection = words_resume.intersection(words_jd)
        return float(len(intersection) / math.sqrt(len(words_resume) * len(words_jd)))

    def predict_ranking_probability(
        self, semantic_score: float, matched_skills_count: int, missing_skills_count: int
    ) -> float:
        if self.xgb_model:
            features = np.array([[semantic_score, matched_skills_count, missing_skills_count]])
            try:
                probabilities = self.xgb_model.predict_proba(features)
                return float(probabilities[0][1])
            except Exception:
                pass
        total_skills = matched_skills_count + missing_skills_count
        skill_ratio = (matched_skills_count / total_skills) if total_skills else 0.5
        calculated_score = (semantic_score * 0.6) + (skill_ratio * 0.4)
        return min(max(float(calculated_score), 0.0), 1.0)
