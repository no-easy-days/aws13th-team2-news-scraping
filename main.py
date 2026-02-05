from fastapi import FastAPI
from routers import articles

from database import Base, engine
from models import Article, Bookmark, User

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(articles.router)