from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from dotenv import load_dotenv

import os

from database import (
    Base,
    engine,
    get_db
)

from models import (
    URL,
    User
)

from schemas import (
    URLCreate
)

from utils import generate_unique_short_code

from security import get_current_user

from auth import router as auth_router


# ==========================================
# Load Environment Variables
# ==========================================

load_dotenv()

BASE_URL = os.getenv("BASE_URL")


# ==========================================
# Database
# ==========================================

Base.metadata.create_all(bind=engine)


# ==========================================
# FastAPI
# ==========================================

app = FastAPI(
    title="URL Shortener API",
    version="1.0"
)


# ==========================================
# Authentication Routes
# ==========================================

app.include_router(auth_router)


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# Home
# ==========================================

@app.get("/")
def home():

    return {
        "message": "Welcome to URL Shortener API"
    }


# ==========================================
# Create URL
# ==========================================

@app.post("/urls")
def create_url(
    url: URLCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    short_code = generate_unique_short_code(db)

    new_url = URL(
        original_url=str(url.original_url),
        short_code=short_code,
        owner_id=current_user.id
    )

    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return {
        "short_url": f"{BASE_URL}/{new_url.short_code}"
    }


# ==========================================
# Get My URLs
# ==========================================

@app.get("/urls")
def get_my_urls(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    urls = db.query(URL).filter(
        URL.owner_id == current_user.id
    ).all()

    return urls


# ==========================================
# Delete URL
# ==========================================

@app.delete("/urls/{url_id}")
def delete_url(
    url_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    url = db.query(URL).filter(
        URL.id == url_id,
        URL.owner_id == current_user.id
    ).first()

    if url is None:
        raise HTTPException(
            status_code=404,
            detail="URL not found"
        )

    db.delete(url)
    db.commit()

    return {
        "message": "URL deleted successfully"
    }


# ==========================================
# Redirect
# ==========================================

@app.get("/{short_code}")
def redirect_url(
    short_code: str,
    db: Session = Depends(get_db)
):

    url = db.query(URL).filter(
        URL.short_code == short_code
    ).first()

    if url is None:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found"
        )

    url.clicks += 1

    db.commit()

    return RedirectResponse(
        url=url.original_url
    )