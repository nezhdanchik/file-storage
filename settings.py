from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CELERY_BROKER_HOST: str
    CELERY_BROKER_PORT: int

    class Config:
        env_file = ".env"

settings = Settings()

def get_celery_broker_url():
    return f"redis://{settings.CELERY_BROKER_HOST}:{settings.CELERY_BROKER_PORT}/0"