from fastapi import APIRouter, Query, HTTPException, Depends, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Article
from backend.utils.search_utils import get_similarity

router = APIRouter()

@router.get("/articles")
def get_articles(
        keyword: str = Query(..., description="검색 키워드"),
        db: Session = Depends(get_db)
):
    clean_keyword = keyword.strip()

    if not clean_keyword:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "INVALID_INPUT", "message": "검색어를 입력해 주세요."}
        )
    if len(clean_keyword) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "error", "message": "검색어는 두 글자 이상 입력해야 합니다."}
        )

    db_articles = db.query(Article).all()
    results = []

    # 2. 모든 기사를 돌면서 유사도 점수(data_score) 계산
    for article in db_articles:
        score = get_similarity(keyword, article.title)
        if score >= 0.01:
            results.append({
                "data_score": round(score, 2),
                "id": article.id,
                "title": article.title,
                "url": article.url,
                "description": article.description,
                "published_at": article.published_at,
                "thumbnail_url": article.thumbnail_url,
                "created_at": article.created_at,
            })

    # 내림 차순으로 정렬
    results.sort(key=lambda x: x["data_score"], reverse=True)
    if len(results) == 0:
        return {
            "status": "NOT_FOUND",  # "success" 대신 명확한 상태 값 부여
            "total_count": 0,
            "data": [],
            "message": f"'{clean_keyword}'에 대한 검색 결과가 없습니다."
        }
    # 기사가 존재했을 때에 대한 return값
    return {
        "status": "success",
        "data": results
    }
