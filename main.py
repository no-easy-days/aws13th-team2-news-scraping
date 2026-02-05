from fastapi import FastAPI
from routers import articles

from database import Base, engine
from routers.bookmark import router as bookmark_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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