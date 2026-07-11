import os

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from xgboost import XGBClassifier


class HybridScoringEngine:
    def __init__(self):
        self.transformer_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.model_path = os.path.join("trained_models", "xgb_resume_ranker.json")
        self.xgb_model = self._load_model()

    def _load_model(self):
        if os.path.exists(self.model_path):
            model = XGBClassifier()
            model.load_model(self.model_path)
            return model
        return None

    def compute_semantic_score(self, resume_text: str, jd_text: str) -> float:
        resume_emb = self.transformer_model.encode([resume_text])
        jd_emb = self.transformer_model.encode([jd_text])
        similarity = cosine_similarity(resume_emb, jd_emb)[0][0]
        return float(similarity)

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
