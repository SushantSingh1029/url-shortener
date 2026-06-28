from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import uuid
from datetime import datetime, timedelta
from app.models.user import User
from app.models.email_token import EmailVerificationToken
from app.models.password_reset import PasswordResetToken
from app.schemas.user import UserCreate
from app.utils.security import hash_password, verify_password
from app.utils.validators import validate_password_strength

def register_user(db: Session, user: UserCreate) -> User:
    if not validate_password_strength(user.password):
        raise HTTPException(status_code=400, detail="Password does not meet strength requirements")
    
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
        
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
        
    hashed_pwd = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def create_verification_token(db: Session, user_id: int) -> str:
    token = str(uuid.uuid4())
    expires = datetime.utcnow() + timedelta(hours=24)
    db_token = EmailVerificationToken(user_id=user_id, token=token, expires_at=expires)
    db.add(db_token)
    db.commit()
    return token

def verify_email(db: Session, token: str) -> bool:
    db_token = db.query(EmailVerificationToken).filter(EmailVerificationToken.token == token).first()
    if not db_token or db_token.verified or db_token.expires_at < datetime.utcnow():
        return False
        
    user = db.query(User).filter(User.id == db_token.user_id).first()
    if user:
        user.is_verified = True
        db_token.verified = True
        db.commit()
        return True
    return False

def create_password_reset_token(db: Session, email: str) -> str:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
        
    token = str(uuid.uuid4())
    expires = datetime.utcnow() + timedelta(hours=1)
    db_token = PasswordResetToken(user_id=user.id, token=token, expires_at=expires)
    db.add(db_token)
    db.commit()
    return token

def reset_password(db: Session, token: str, new_password: str) -> bool:
    if not validate_password_strength(new_password):
        raise HTTPException(status_code=400, detail="Password does not meet strength requirements")
        
    db_token = db.query(PasswordResetToken).filter(PasswordResetToken.token == token).first()
    if not db_token or db_token.used or db_token.expires_at < datetime.utcnow():
        return False
        
    user = db.query(User).filter(User.id == db_token.user_id).first()
    if user:
        user.hashed_password = hash_password(new_password)
        db_token.used = True
        db.commit()
        return True
    return False
