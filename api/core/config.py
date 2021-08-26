import secrets

from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    FIRST_USER: str = 'admin@admin.co'
    FIRST_USER_PWD: str = 'admin@admin.co'
    CELERY_BROKER: str = 'redis://localhost'
    CELERY_BACKEND: str = 'redis://localhost'


settings = Settings()
