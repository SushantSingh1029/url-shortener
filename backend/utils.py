import random
import string

from sqlalchemy.orm import Session

from models import URL


# =====================================
# Generate Random Short Code
# =====================================

def generate_short_code(length: int = 6):

    characters = string.ascii_letters + string.digits

    return "".join(
        random.choices(
            characters,
            k=length
        )
    )


# =====================================
# Generate Unique Short Code
# =====================================

def generate_unique_short_code(
    db: Session,
    length: int = 6
):

    while True:

        short_code = generate_short_code(length)

        existing = db.query(URL).filter(
            URL.short_code == short_code
        ).first()

        if existing is None:
            return short_code