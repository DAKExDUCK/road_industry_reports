from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "road_industry_reports"
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/reports"
    SECRET_KEY: str = "change-me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"

settings = Settings()
