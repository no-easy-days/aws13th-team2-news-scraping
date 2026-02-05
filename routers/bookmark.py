from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
from repositories.bookmark_repository import BookmarkRepository

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


