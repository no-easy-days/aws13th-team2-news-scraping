from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.article import Article
from schemas.article import ArticleCreate


class ArticleRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, article: ArticleCreate) -> Article | None:
        """기사 생성. 중복(url)이면 None 반환."""
        db_article = Article(
            title=article.title,
            url=str(article.url),
            content=article.content,
            published_at=article.published_at,
            thumbnail_url=str(article.thumbnail_url) if article.thumbnail_url else None,
        )
        try:
            self.db.add(db_article)
            self.db.commit()
            self.db.refresh(db_article)
            return db_article
        except IntegrityError:
            self.db.rollback()
            return None

    def bulk_create(self, articles: list[ArticleCreate]) -> tuple[int, int]:
        """
        여러 기사 일괄 저장.

        Returns:
            (성공 개수, 중복 개수)
        """
        success = 0
        duplicate = 0
        for article in articles:
            result = self.create(article)
            if result:
                success += 1
            else:
                duplicate += 1
        return success, duplicate
