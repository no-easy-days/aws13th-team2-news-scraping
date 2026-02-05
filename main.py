import logging
from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

from crawler.mk_news import crawl_mk_news, save_to_db
from database import Base, engine
from routers import articles
from routers.bookmark import router as bookmark_router

logger = logging.getLogger(__name__)


def run_crawler():
    """스케줄러에서 호출하는 크롤러 실행 함수"""
    logger.info("스케줄러: 크롤링 시작")
    articles = crawl_mk_news(days=1)
    success, duplicate = save_to_db(articles)
    logger.info("스케줄러: 크롤링 완료 - 신규 %d건, 중복 %d건", success, duplicate)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 시작 시
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_crawler, "interval", minutes=30)
    scheduler.start()
    logger.info("스케줄러 시작 (30분 간격)")

    run_crawler()  # 시작 시 즉시 1회 실행

    yield

    # 서버 종료 시
    scheduler.shutdown()
    logger.info("스케줄러 종료")


app = FastAPI(lifespan=lifespan)

Base.metadata.create_all(bind=engine)

app.include_router(articles.router)
app.include_router(bookmark_router)
