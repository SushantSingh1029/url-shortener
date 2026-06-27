from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from dotenv import load_dotenv
import os

from database import Base, engine, get_db
from models import URL
from schemas import URLCreate
from utils import generate_short_code

# -------------------------------
# Load Environment Variables
# -------------------------------
load_dotenv()

BASE_URL = os.getenv("BASE_URL")

# -------------------------------
# Create database tables
# -------------------------------
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "URL Shortener API"}


@app.post("/urls")
def create_url(
    url: URLCreate,
    db: Session = Depends(get_db)
):

    new_url = URL(
        original_url=str(url.original_url),
        short_code=generate_short_code()
    )

    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return {
        "short_url": f"{BASE_URL}/{new_url.short_code}"
    }


@app.get("/{short_code}")
def redirect_to_url(
    short_code: str,
    db: Session = Depends(get_db)
):

    url = db.query(URL).filter(
        URL.short_code == short_code
    ).first()

    if not url:
        return {"error": "Short URL not found"}

    return RedirectResponse(url=url.original_url)