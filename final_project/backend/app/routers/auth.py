from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

from app.database import db_helper
from app.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])


class RegisterRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    name: str
    email: EmailStr


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest):
    existing = await db_helper.db.users.find_one({"email": payload.email.lower()})
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="An account with this email already exists.")

    user_doc = {
        "name": payload.name.strip(),
        "email": payload.email.lower(),
        "password_hash": hash_password(payload.password),
    }
    result = await db_helper.db.users.insert_one(user_doc)
    token = create_access_token(str(result.inserted_id), user_doc["name"])
    return TokenResponse(access_token=token, name=user_doc["name"], email=user_doc["email"])


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest):
    user = await db_helper.db.users.find_one({"email": payload.email.lower()})
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password.")

    token = create_access_token(str(user["_id"]), user.get("name", "Candidate"))
    return TokenResponse(access_token=token, name=user.get("name", "Candidate"), email=user["email"])
