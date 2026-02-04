import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()


def _build_database_url() -> str:
    # Priority: explicit URL -> MariaDB-style env vars
    db_url = os.getenv("DB_URL") or os.getenv("DATABASE_URL")
    if db_url:
        return db_url

    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    name = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    required = {
        "DB_HOST": host,
        "DB_PORT": port,
        "DB_NAME": name,
        "DB_USER": user,
        "DB_PASSWORD": password,
    }
    missing = [k for k, v in required.items() if not v]
    if missing:
        raise ValueError(
            "데이터베이스 설정이 누락되었습니다. "
            "DB_URL(또는 DATABASE_URL)을 설정하거나, "
            "DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD를 모두 설정해주세요. "
            f"누락 항목: {', '.join(missing)}"
        )

    safe_password = quote_plus(password)
    return f"mysql+pymysql://{user}:{safe_password}@{host}:{port}/{name}"


DATABASE_URL = _build_database_url()

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
