from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError, DatabaseError
from backend.database import get_db
from backend.repositories.bookmark_repository import (BookmarkRepository)

router = APIRouter(prefix="/articles", tags=["Bookmark"])

TEST_USER_ID = 1

@router.post("/{article_id}/bookmark")
async def toggle_bookmark(
        article_id: int,
        db: Session = Depends(get_db)
):
    repo = BookmarkRepository(db)

    # 1. 기존 북마크 여부 확인
    existing_bookmark = repo.get_bookmark(TEST_USER_ID, article_id)

    if existing_bookmark:
        try:
            repo.delete_bookmark(existing_bookmark)
            return {
                "status": "success",
                "message": "북마크가 해제되었습니다.",
                "is_bookmarked": False
            }
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="서버 내부 오류가 발생했습니다."
            )


    # 3. 없으면 추가 (Toggle On)
    try:
        repo.create_bookmark(TEST_USER_ID, article_id)
        return {
            "status": "success",
            "message": "북마크가 추가되었습니다.",
            "is_bookmarked": True
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"article_id {article_id}에 해당하는 기사를 찾을 수 없습니다."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="서버 내부 오류가 발생했습니다."
        )

@router.get("/bookmarks")
async def get_bookmarks(db: Session = Depends(get_db)):
    """현재 사용자의 북마크 목록 조회"""
    repo = BookmarkRepository(db)

    try:
        bookmarks = repo.get_user_bookmarks(TEST_USER_ID)

        # 북마크가 없는 경우
        if not bookmarks:
            return {
                "status": "success",
                "total_count": 0,
                "data": [],
                "message": "북마크한 기사가 없습니다."
            }

        results = []
        for bookmark in bookmarks:
            try:
                # 각 북마크별로 article 접근 시도
                article = bookmark.article

                # article이 삭제되었을 경우 대비
                if not article:
                    continue

                results.append({
                    "bookmark_id": bookmark.id,
                    "bookmarked_at": bookmark.saved_at,
                    "article": {
                        "id": article.id,
                        "title": article.title,
                        "url": article.url,
                        "content": getattr(article, 'content', None),  # content 없을 경우 대비
                        "published_at": article.published_at,
                        "thumbnail_url": article.thumbnail_url,
                        "created_at": article.created_at,
                    }
                })
            except AttributeError:
                # article 관계 로딩 실패 (기사가 삭제된 경우)
                continue

        return {
            "status": "success",
            "total_count": len(results),
            "data": results
        }

    except OperationalError:
        # DB 연결 오류
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="데이터베이스 연결에 실패했습니다."
        )
    except DatabaseError:
        # 쿼리 실행 오류
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="데이터베이스 조회 중 오류가 발생했습니다."
        )
    except Exception as e:
        # 기타 예상치 못한 오류
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="북마크 목록 조회 중 오류가 발생했습니다."
        )


