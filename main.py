from fastapi import FastAPI
from routers import articles

from database import Base, engine
from routers.bookmark import router as bookmark_router
from models import Article, Bookmark, User

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(articles.router)
app.include_router(bookmark_router)
