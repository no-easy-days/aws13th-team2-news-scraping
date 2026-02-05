from fastapi import FastAPI, APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Article
from utils.search_utils import get_similarity
from datetime import datetime

router = APIRouter()

# 1. 테스트용 기사 데이터 (나중에 DB 연결 시 삭제)
# MOCK_ARTICLES = [
#     {
#         "id": 1,
#         "title": "AI 반도체 시장의 미래와 엔비디아의 전략",
#         "url": "https://news.example.com/ai-semiconductor-future",
#         "content": "인공지능 반도체 시장이 급격히 성장하면서 엔비디아의 독주 체제가 이어지고 있습니다...",
#         "published_at": datetime(2026, 2, 4, 10, 0, 0),
#         "thumbnail_url": "https://news.example.com/thumb/1.jpg",
#         "created_at": datetime.utcnow()
#     },
#     {
#         "id": 2,
#         "title": "FastAPI를 활용한 마이크로서비스 아키텍처 구축",
#         "url": "https://tech.example.com/fastapi-msa",
#         "content": "최근 백엔드 개발에서 FastAPI는 빠른 성능과 생산성으로 큰 인기를 끌고 있습니다...",
#         "published_at": datetime(2026, 2, 4, 11, 30, 0),
#         "thumbnail_url": None,  # nullable=True 반영
#         "created_at": datetime.utcnow()
#     },
#     {
#         "id": 3,
#         "title": "2026년 클라우드 컴퓨팅 트렌드 분석",
#         "url": "https://cloud.example.com/trends-2026",
#         "content": "멀티 클라우드와 서버리스 컴퓨팅이 기업들의 핵심 전략으로 자리 잡으면서...",
#         "published_at": datetime(2026, 2, 3, 15, 0, 0),
#         "thumbnail_url": "https://cloud.example.com/thumb/3.jpg",
#         "created_at": datetime.utcnow()
#     }
# ]

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
