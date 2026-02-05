from fastapi import FastAPI, APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Article
from utils.search_utils import get_similarity
from datetime import datetime

router = APIRouter()

@router.get("/articles")
async def get_articles(
        keyword: str = Query(..., description="검색 키워드"),
        db: Session = Depends(get_db)
):
    if not keyword.strip():
        raise HTTPException(
            status_code=422,
            detail={
                "status": "error",
                "message": "검색어를 입력해주세요."
            }
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
                "content": article.content,
                "published_at": article.published_at,
                "thumbnail_url": article.thumbnail_url,
                "created_at": article.created_at,
            })

    # 내림 차순으로 정렬
    results.sort(key=lambda x: x["data_score"], reverse=True)
    if len(results) == 0:
        return {
            "status": "success",
            "data": [],
            "message": "일치하는 기사가 없습니다. 다른 검색어를 입력해 보세요."
        }

    return {
        "status": "success",
        "data": results
    }
