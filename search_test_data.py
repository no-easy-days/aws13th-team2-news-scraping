from database import SessionLocal
from models import Article
from datetime import datetime, timedelta


def insert_test_articles():
    db = SessionLocal()
    try:
        # 1. 기존 테스트 데이터와 겹치지 않게 샘플 데이터 구성
        test_data = [
            {
                "title": "경기대학교 AI컴공 프로젝트 중간 점검",
                "url": "https://kgu.ac.kr/news/1",
                "content": "FastAPI와 MariaDB를 활용한 뉴스 검색 서비스 개발이 한창입니다.",
                "published_at": datetime.now()
            },
            {
                "title": "2026년 파이썬 반도체 시장 전망 보고서",
                "url": "https://kgu.ac.kr/news/2",
                "content": "엔비디아와 삼성전자의 차세대 칩 경쟁이 치열해질 것으로 보입니다.",
                "published_at": datetime.now() - timedelta(days=1)
            },
            {
                "title": "파이썬 크롤링 기초부터 실전까지",
                "url": "https://kgu.ac.kr/news/3",
                "content": "BeautifulSoup을 이용하면 누구나 쉽게 웹 데이터를 수집할 수 있습니다.",
                "published_at": datetime.now() - timedelta(days=2)
            }
        ]

        for data in test_data:
            # 중복 URL 체크 (이미 있으면 건너뜀)
            exists = db.query(Article).filter(Article.url == data["url"]).first()
            if not exists:
                article = Article(**data)
                db.add(article)

        db.commit()
        print("✅ 테스트 데이터 삽입 성공! DataGrip에서 확인하세요.")

    except Exception as e:
        db.rollback()
        print(f"❌ 오류 발생: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    insert_test_articles()