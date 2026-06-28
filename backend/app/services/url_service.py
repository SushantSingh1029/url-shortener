from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
from app.models.url import URL
from app.schemas.url import URLCreate, URLUpdate
from app.utils.shortener import generate_unique_short_code
from app.models.user import User

def create_url(db: Session, url_in: URLCreate, user: User) -> URL:
    if url_in.custom_alias:
        if db.query(URL).filter(URL.custom_alias == url_in.custom_alias).first():
            raise HTTPException(status_code=400, detail="Custom alias already in use")
        short_code = url_in.custom_alias
    else:
        short_code = generate_unique_short_code(db)
        
    new_url = URL(
        owner_id=user.id,
        original_url=str(url_in.original_url),
        short_code=short_code,
        custom_alias=url_in.custom_alias,
        expires_at=url_in.expires_at
    )
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url

def get_url(db: Session, short_code: str) -> URL:
    return db.query(URL).filter(URL.short_code == short_code).first()

def get_user_urls(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(URL).filter(URL.owner_id == user_id).offset(skip).limit(limit).all()

def update_url(db: Session, url_id: int, user_id: int, update_data: URLUpdate) -> Optional[URL]:
    db_url = db.query(URL).filter(URL.id == url_id, URL.owner_id == user_id).first()
    if not db_url:
        return None
        
    if update_data.custom_alias and update_data.custom_alias != db_url.short_code:
        # Check collision
        existing = db.query(URL).filter(URL.short_code == update_data.custom_alias).first()
        if existing:
            raise ValueError("Custom alias already in use")
        db_url.short_code = update_data.custom_alias
        
    if update_data.original_url:
        db_url.original_url = str(update_data.original_url)
        
    # Checking against None directly isn't enough if they pass null to unset it, 
    # but Pydantic's Optional treats omitted fields as None. 
    # For a real patch update, exclude_unset should be used, but this suffices for now.
    if update_data.expires_at:
        db_url.expires_at = update_data.expires_at
        
    db.commit()
    db.refresh(db_url)
    return db_url

def delete_url(db: Session, url_id: int, user_id: int):
    url = db.query(URL).filter(URL.id == url_id, URL.owner_id == user_id).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    db.delete(url)
    db.commit()
