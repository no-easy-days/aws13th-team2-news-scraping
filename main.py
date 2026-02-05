from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

from crawler.mk_news import crawl_mk_news, save_to_db
from database import Base, engine
from routers import articles
from routers.bookmark import router as bookmark_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_crawler():
    """스케줄러에서 호출하는 크롤러 실행 함수"""
    articles = crawl_mk_news(days=1)
    success, duplicate = save_to_db(articles)
    logger.info("스케줄러: 크롤링 완료 - 신규 %d건, 중복 %d건", success, duplicate)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 시작 시
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_crawler, "interval", minutes=30, next_run_time=datetime.now())
    scheduler.start()

    yield

    # 서버 종료 시
    scheduler.shutdown()
    logger.info("스케줄러 종료")


app = FastAPI(lifespan=lifespan)

Base.metadata.create_all(bind=engine)

app.include_router(articles.router)
app.include_router(bookmark_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 앱 주소
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

Base.metadata.create_all(bind=engine)

app.include_router(articles.router)
app.include_router(bookmark_router)
