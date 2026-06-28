from pydantic import BaseModel, HttpUrl, Field, ConfigDict
from datetime import datetime
from typing import Optional

class URLBase(BaseModel):
    original_url: HttpUrl

class URLCreate(BaseModel):
    original_url: HttpUrl
    custom_alias: Optional[str] = Field(None, min_length=3, max_length=50)
    expires_at: Optional[datetime] = None

class URLUpdate(BaseModel):
    original_url: Optional[HttpUrl] = None
    custom_alias: Optional[str] = Field(None, min_length=3, max_length=50)
    expires_at: Optional[datetime] = None

class URLResponse(BaseModel):
    id: int
    original_url: HttpUrl
    short_code: str
    custom_alias: Optional[str] = None
    clicks: int
    created_at: datetime
    updated_at: datetime
    expires_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
