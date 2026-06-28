from fastapi import APIRouter, Depends
from app.schemas.user import UserResponse
from app.dependencies import get_current_user
from app.models.user import User
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.url import URL

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/me/analytics")
def get_analytics(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    urls = db.query(URL).filter(URL.owner_id == current_user.id).all()
    total_urls = len(urls)
    total_clicks = sum(url.clicks for url in urls)
    most_clicked = max(urls, key=lambda u: u.clicks, default=None)
    
    return {
        "total_urls": total_urls,
        "total_clicks": total_clicks,
        "most_clicked_url": most_clicked.short_code if most_clicked else None,
    }
