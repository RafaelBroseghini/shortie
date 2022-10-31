from pydantic import BaseSettings


class Settings(BaseSettings):
    CACHE_TTL: int = 3600


settings = Settings()
