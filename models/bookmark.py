from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.sql import func
# database.py 담당자가 만든 Base를 임포트 (경로는 프로젝트 상황에 맞게 수정)
from database import Base

class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    # article_id는 기사 테이블의 id를 참조
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False)
    # user_id는 담당자가 넣어줄 테스트 유저(id=1 등)의 id를 참조
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    saved_at = Column(DateTime(timezone=True), server_default=func.now())

    # 한 유저가 같은 기사를 여러 번 북마크하는 것 방지 (DB 무결성)
    __table_args__ = (UniqueConstraint('user_id', 'article_id', name='_user_article_uc'),)