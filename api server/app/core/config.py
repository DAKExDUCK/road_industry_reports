from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "road_industry_reports"
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/reports"
    SECRET_KEY: str = "change-me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # root admin seeded on startup (optional)
    root_admin_email: Optional[str] = None
    root_admin_password: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()
