# app/models/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class ThumbnailRequest(BaseModel):
    title: str
    description: Optional[str] = ""
    genre: str
    style: Optional[str] = "modern"
    color_scheme: Optional[str] = "vibrant"

class ThumbnailResponse(BaseModel):
    success: bool
    # thumbnail_id: Optional[int] = None
    image_url: str
    download_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    # prompt_used: str
    # suggestions: List[str]
    generation_time: Optional[float] = None

class UserDashboard(BaseModel):
    user: dict
    recent_thumbnails: List[dict]
    genre_stats: List[dict]

class EmailRequest(BaseModel):
    email: EmailStr
    subject: str
    message: str