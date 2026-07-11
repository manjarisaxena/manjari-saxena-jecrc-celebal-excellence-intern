# HireSense AI — Resume Screening Assistant

Full-stack app: FastAPI + MongoDB backend, React (Vite) frontend.

## What changed from the original blueprint

The original `unpack_gravity.py` / `project.md` blueprint had two problems that are fixed here:

1. **No real authentication.** The old `/auth/token` endpoint handed out a valid login token to anyone, no credentials checked. This build adds real `POST /auth/register` and `POST /auth/login` endpoints backed by a MongoDB `users` collection with bcrypt-hashed passwords.
2. **Hardcoded secrets in `docker-compose.yml`.** Secrets now come from a `.env` file (never committed) instead of being written into the compose file.

## Project structure

```
backend/     FastAPI app (auth, resume parsing, matching, RAG feedback, chatbot)
frontend/    React + Vite app (login, evaluate, history, chat)
docker-compose.yml
```

## Run with Docker (easiest)

1. Copy the env template and fill in real values:
   ```bash
   cp backend/.env.example backend/.env
   ```
   Edit `backend/.env`:
   - `JWT_SECRET` — any long random string (e.g. `openssl rand -hex 32`)
   - `GOOGLE_API_KEY` — a Gemini API key from https://aistudio.google.com/app/apikey (optional — without it, feedback falls back to a plain missing-skills list and the chat endpoint returns an error)

2. Start everything:
   ```bash
   docker-compose up --build
   ```

3. Open the app: **http://localhost:5173**
   API docs (Swagger): **http://localhost:8000/docs**

## Run without Docker

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
cp .env.example .env   # then edit JWT_SECRET / GOOGLE_API_KEY
# Make sure MongoDB is running locally, or update MONGO_URI in .env
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env   # VITE_API_URL defaults to http://localhost:8000
npm run dev
```

## First use

1. Open the frontend, click **Sign up**, create an account (name, email, password ≥ 8 chars).
2. Go to **Evaluate**, paste a job description, upload a resume (`.pdf`, `.docx`, or `.txt`), click **Run evaluation**.
3. Check **History** for past evaluations, or **Chat** to ask follow-up questions.

## Notes

- The resume-ranking model (`trained_models/xgb_resume_ranker.json`) is optional — if it's not present, the app falls back to a rule-based score (semantic similarity + skill overlap), so the app works out of the box without a pretrained model.
- CORS in `backend/app/main.py` is currently open to `localhost:5173` only — update `allow_origins` if you deploy the frontend elsewhere.
- Don't commit `backend/.env` or `frontend/.env` — they're already in `.gitignore`.
