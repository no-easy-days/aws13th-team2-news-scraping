from datetime import datetime
from pydantic import BaseModel, HttpUrl


class ArticleCreate(BaseModel):
    """크롤링한 기사 데이터를 검증하는 스키마"""
    title: str
    url: HttpUrl
    content: str | None = None
    published_at: datetime
    thumbnail_url: HttpUrl | None = None


class ArticleResponse(BaseModel):
    """API 응답용 기사 스키마"""
    id: int
    title: str
    url: str
    content: str | None
    published_at: datetime
    thumbnail_url: str | None
    created_at: datetime

    class Config:
        from_attributes = True
