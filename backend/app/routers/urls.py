from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.url import URLCreate, URLResponse, URLUpdate
from app.services.url_service import create_url, get_user_urls, delete_url, update_url
from app.dependencies import get_current_user
from app.models.user import User
from typing import List

router = APIRouter(prefix="/urls", tags=["URLs"])

@router.post("/", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
def create(url_in: URLCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_url(db, url_in, current_user)

@router.get("/", response_model=List[URLResponse])
def read_user_urls(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_user_urls(db, current_user.id)

@router.put("/{url_id}", response_model=URLResponse)
def update_existing_url(
    url_id: int, 
    update_data: URLUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    try:
        updated_url = update_url(db, url_id, current_user.id, update_data)
        if not updated_url:
            raise HTTPException(status_code=404, detail="URL not found or unauthorized")
        return updated_url
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{url_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(url_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    delete_url(db, url_id, current_user.id)
