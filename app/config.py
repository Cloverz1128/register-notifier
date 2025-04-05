from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    FRONTEND_ORIGIN: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"  # set .env

settings = Settings()