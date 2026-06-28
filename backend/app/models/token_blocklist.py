from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class TokenBlocklist(Base):
    __tablename__ = "token_blocklist"
    
    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
