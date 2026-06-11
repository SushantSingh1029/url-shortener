from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from database import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)

    original_url = Column(String, nullable=False)

    short_code = Column(
        String,
        unique=True,
        nullable=False
    )

    clicks = Column(
        Integer,
        default=0
    )