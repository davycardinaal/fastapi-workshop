from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: str = "http://localhost:3000, https://todo.formatics.nl, https://todo.kabisa.nl"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "workshop"
    POSTGRES_PASSWORD: str = "workshop"
    POSTGRES_DB: str = "workshop"
    DATABASE_URI: PostgresDsn = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"  # type: ignore
