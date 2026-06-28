# Full Stack URL Shortener (Production Ready)

This is a production-grade URL shortener application refactored to use a modular FastAPI architecture with PostgreSQL on the backend, and a React + Tailwind CSS dashboard on the frontend.

## Tech Stack
- **Backend**: Python 3.12, FastAPI, SQLAlchemy (PostgreSQL), Alembic, Pydantic, JWT Auth
- **Frontend**: React, Vite, Tailwind CSS, Context API

## Deployment Guidelines

### Backend (Render)
1. Set the environment variables in the Render dashboard (see `backend/.env.example`).
2. Build command: `cd backend && pip install -r requirements.txt`
3. Start command: `cd backend && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Attach a Render PostgreSQL database and set the `DATABASE_URL` appropriately.

### Frontend (Vercel)
1. Set `VITE_API_URL` to your Render backend URL (e.g., `https://your-backend.onrender.com/api`).
2. Build command: `cd frontend && npm install && npm run build`
3. Output directory: `frontend/dist`

## Local Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # Fill in your local DB credentials
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
