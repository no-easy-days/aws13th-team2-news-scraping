from sqlalchemy.orm import Session
from models.bookmark import Bookmark

class BookmarkRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_bookmark(self, user_id: int, article_id: int):
        """특정 유저가 특정 기사를 북마크했는지 조회"""
        return self.db.query(Bookmark).filter(
            Bookmark.user_id == user_id,
            Bookmark.article_id == article_id
        ).first()

    def create_bookmark(self, user_id: int, article_id: int):
        """북마크 생성"""
        db_bookmark = Bookmark(user_id=user_id, article_id=article_id)
        self.db.add(db_bookmark)
        self.db.commit()
        return db_bookmark

    def delete_bookmark(self, bookmark: Bookmark):
        """북마크 삭제"""
        self.db.delete(bookmark)
        self.db.commit()
        return True