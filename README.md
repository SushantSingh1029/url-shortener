# 🔗 URL Shortener

A full-stack URL Shortener built with **FastAPI**, **React (Vite)**, **PostgreSQL**, and **JWT Authentication**. Users can securely register, log in, create short URLs, manage them through a dashboard, and track click analytics.

---

## 🚀 Live Demo

### Frontend
https://url-shortener-one-kappa-97.vercel.app/

### Backend API
https://url-shortener-tiij.onrender.com

### API Documentation
https://url-shortener-tiij.onrender.com/docs

---

# ✨ Features

- 🔐 JWT Authentication
- 👤 User Registration & Login
- 🔄 Access & Refresh Tokens
- 🔗 Create Short URLs
- 🏷️ Custom Short Alias Support
- 📊 Click Analytics
- 📋 Copy Short URL
- 🗑️ Delete URLs
- 🛡️ Protected Dashboard
- 📱 Responsive UI
- ☁️ Cloud Deployment

---

# 🛠 Tech Stack

## Frontend

- React
- Vite
- React Router
- Axios
- Tailwind CSS

## Backend

- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- JWT Authentication
- Passlib (bcrypt)

## Deployment

- Vercel (Frontend)
- Render (Backend)
- Render PostgreSQL

---

---

# Authentication Flow

```
Register
      │
      ▼
Login
      │
      ▼
Access Token + Refresh Token
      │
      ▼
Protected Dashboard
      │
      ├── Create URL
      ├── Delete URL
      ├── View Analytics
      └── Logout
```

---

# API Endpoints

## Authentication

| Method | Endpoint |
|---------|----------|
| POST | `/api/auth/register` |
| POST | `/api/auth/login` |
| POST | `/api/auth/refresh` |
| POST | `/api/auth/logout` |

---

## URL Management

| Method | Endpoint |
|---------|----------|
| POST | `/api/urls` |
| GET | `/api/urls` |
| DELETE | `/api/urls/{id}` |
| GET | `/{short_code}` |

---

# Local Installation

## Clone Repository

```bash
git clone https://github.com/SushantSingh1029/url-shortener.git

cd url-shortener
```

---

# Backend Setup

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env`

```env
DATABASE_URL=

SECRET_KEY=

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

REFRESH_TOKEN_EXPIRE_DAYS=7

BASE_URL=http://localhost:8000
```

Run backend

```bash
uvicorn app.main:app --reload
```

---

# Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Create `.env`

```env
VITE_API_URL=http://localhost:8000/api
```

---

# Database Migration

```bash
alembic upgrade head
```

---

# Deployment

## Backend

- Render Web Service
- Render PostgreSQL

## Frontend

- Vercel

Environment Variable

```env
VITE_API_URL=https://url-shortener-tiij.onrender.com/api
```

---

# Screenshots

Add screenshots of:

- Login Page
- Register Page
- Dashboard
- URL Management

---

# Future Improvements

- Email Verification
- Password Reset via Email
- QR Code Generation
- URL Expiration
- Password-Protected URLs
- Custom Domains
- Rate Limiting
- Admin Dashboard
- Advanced Analytics

---

# Demo Notes

- Email verification and password reset email delivery are temporarily disabled in the deployed demo because outbound SMTP email delivery is not configured for the hosting environment.
- Registration, login, JWT authentication, URL shortening, analytics, and dashboard functionality are fully operational.

---

# Author

**Sushant Singh**

GitHub:  
https://github.com/SushantSingh1029

LinkedIn:  
https://linkedin.com/in/sushant-sushant-4421513ab

---

## ⭐ If you found this project useful, consider giving it a star!
