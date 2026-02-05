from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Bookmark(Base):
    __tablename__ = "bookmarks"
    __table_args__ = (UniqueConstraint("article_id", "user_id", name="uq_bookmarks_user_article"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    saved_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    article = relationship("Article", back_populates="bookmarks")
    user = relationship("User", back_populates="bookmarks")

