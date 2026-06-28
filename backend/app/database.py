from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# Strict PostgreSQL engine creation with production connection pooling
engine = create_engine(
    str(settings.DATABASE_URL),
    pool_size=10,          # Limit standing connections
    max_overflow=20,       # Max connections above pool_size during traffic spikes
    pool_pre_ping=True,    # Verify connection health before using
    pool_recycle=1800      # Recycle connections every 30 minutes to avoid DB disconnects
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
