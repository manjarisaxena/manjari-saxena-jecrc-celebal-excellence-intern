from datetime import datetime, timezone

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from app.auth import get_current_user
from app.database import db_helper
from app.services.matcher import HybridScoringEngine
from app.services.parser import ResumeParser
from app.services.rag_feedback import ExplainableAIEngine

router = APIRouter(prefix="/resumes", tags=["Resume Evaluation"])

ai_engine = HybridScoringEngine()
rag_engine = ExplainableAIEngine()

ALLOWED_EXTENSIONS = (".pdf", ".docx", ".txt")


@router.post("/evaluate")
async def evaluate_resume(
    file: UploadFile = File(...),
    jd_title: str = Form(...),
    jd_text: str = Form(...),
    current_user: dict = Depends(get_current_user),
):
    if not file.filename.lower().endswith(ALLOWED_EXTENSIONS):
        raise HTTPException(status_code=400, detail="Only .pdf, .docx, or .txt resumes are supported.")

    contents = await file.read()
    parsed_text = ResumeParser.extract_text(contents, file.filename)
    if not parsed_text.strip():
        raise HTTPException(status_code=422, detail="Could not extract any text from this file.")

    extracted_skills = ResumeParser.extract_skills(parsed_text)
    jd_skills = ResumeParser.extract_skills(jd_text)

    matched_skills = [s for s in extracted_skills if s in jd_skills]
    missing_skills = [s for s in jd_skills if s not in extracted_skills]

    semantic_similarity = ai_engine.compute_semantic_score(parsed_text, jd_text)
    ats_match_percentage = round(semantic_similarity * 100, 1)

    ml_rank_probability = ai_engine.predict_ranking_probability(
        semantic_similarity, len(matched_skills), len(missing_skills)
    )
    explainable_feedback = rag_engine.generate_rag_feedback(parsed_text, missing_skills)

    evaluation_payload = {
        "user_id": current_user["_id"],
        "candidate_name": current_user["name"],
        "job_title": jd_title,
        "ats_score": ats_match_percentage,
        "ml_rank_confidence": round(ml_rank_probability * 100, 1),
        "skills_match": matched_skills,
        "skills_missing": missing_skills,
        "explainable_feedback": explainable_feedback,
        "processed_at": datetime.now(timezone.utc),
    }
    result = await db_helper.db.evaluations.insert_one(dict(evaluation_payload))
    evaluation_payload["_id"] = str(result.inserted_id)
    evaluation_payload["processed_at"] = evaluation_payload["processed_at"].isoformat()
    return evaluation_payload


@router.get("/history")
async def get_history(current_user: dict = Depends(get_current_user)):
    cursor = db_helper.db.evaluations.find({"user_id": current_user["_id"]}).sort("processed_at", -1)
    items = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        doc["processed_at"] = doc["processed_at"].isoformat()
        items.append(doc)
    return items
