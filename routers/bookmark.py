from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db # DB 담당자가 만든 세션 관리 함수
from repositories.bookmark_repository import bookmark_repository

router = APIRouter(prefix="/articles", tags=["Bookmark"])

# 테스트 유저 ID 설정 (나중에 유저 로직 완성 시 Depends로 교체)
TEST_USER_ID = 1

@router.post("/{article_id}/bookmark")
async def toggle_bookmark(
        article_id: int,
        db: Session = Depends(get_db)
):
    repo = bookmark_repository(db)

    # 1. 기존 북마크 여부 확인
    existing_bookmark = repo.get_bookmark(TEST_USER_ID, article_id)

    if existing_bookmark:
        # 2. 이미 있으면 삭제 (Toggle Off)
        repo.delete_bookmark(existing_bookmark)
        return {
            "status": "success",
            "message": "북마크가 해제되었습니다.",
            "is_bookmarked": False
        }

    # 3. 없으면 추가 (Toggle On)
    try:
        repo.create_bookmark(TEST_USER_ID, article_id)
        return {
            "status": "success",
            "message": "북마크가 추가되었습니다.",
            "is_bookmarked": True
        }
    except Exception as e:
        # DB 담당자가 article 테이블을 아직 안 만들었거나,
        # article_id가 실제 DB에 없을 경우 에러 발생
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="북마크 처리에 실패했습니다. 기사 ID를 확인하세요."
        )