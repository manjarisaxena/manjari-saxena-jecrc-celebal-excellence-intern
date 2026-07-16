from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.auth import get_current_user
from app.config import settings

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


class ChatQuery(BaseModel):
    message: str = Field(min_length=1, max_length=2000)


@router.post("/chat")
async def process_chat_interaction(query: ChatQuery, current_user: dict = Depends(get_current_user)):
    if not settings.GOOGLE_API_KEY:
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY is not configured on the server.")

    from langchain_google_genai import ChatGoogleGenerativeAI

    llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", google_api_key=settings.GOOGLE_API_KEY)
    prompt_context = (
        "You are the HireSense AI assistant, helping a candidate understand resume "
        f"screening results and career advice. Candidate name: {current_user['name']}. "
        f"Question: {query.message}"
    )
    response = llm.invoke(prompt_context)
    return {"response": response.content}
