from urllib.parse import quote_plus

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DB_URL: str | None = None
    DATABASE_URL: str | None = None

    DB_HOST: str | None = None
    DB_PORT: int | None = None
    DB_NAME: str | None = None
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None

    @computed_field  # type: ignore[prop-decorator]
    @property
    def database_url(self) -> str:
        if self.DB_URL:
            return self.DB_URL
        if self.DATABASE_URL:
            return self.DATABASE_URL

        required = {
            "DB_HOST": self.DB_HOST,
            "DB_PORT": self.DB_PORT,
            "DB_NAME": self.DB_NAME,
            "DB_USER": self.DB_USER,
            "DB_PASSWORD": self.DB_PASSWORD,
        }
        missing = [k for k, v in required.items() if v in (None, "")]
        if missing:
            raise ValueError(
                "데이터베이스 설정이 누락되었습니다. "
                "DB_URL(또는 DATABASE_URL)을 설정하거나 "
                "DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD를 모두 설정해주세요. "
                f"누락 항목: {', '.join(missing)}"
            )

        password = quote_plus(str(self.DB_PASSWORD))
        return (
            f"mysql+pymysql://{self.DB_USER}:{password}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
