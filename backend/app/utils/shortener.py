import string
import random
from sqlalchemy.orm import Session
from app.models.url import URL

def generate_random_short_code(length: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def generate_unique_short_code(db: Session, length: int = 6) -> str:
    while True:
        code = generate_random_short_code(length)
        if not db.query(URL).filter(URL.short_code == code).first():
            return code
