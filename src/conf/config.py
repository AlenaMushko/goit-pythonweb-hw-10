from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_CONTAINER_NAME: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    POSTGRES_PORT: str = "5432"

    DATABASE_URL: str

    APP_CONTAINER_NAME: str
    APP_HOST: str
    APP_PORT: str = "8000"


settings = Settings()