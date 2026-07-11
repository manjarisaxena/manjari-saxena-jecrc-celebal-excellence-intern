import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import close_mongo_connection, connect_to_mongo
from app.routers import auth, chatbot, resumes


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0", lifespan=lifespan)

# CORS: localhost for dev, plus any extra origins from env (e.g. your Vercel URL) for production.
extra_origins = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", *extra_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(resumes.router)
app.include_router(chatbot.router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
