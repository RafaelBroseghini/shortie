from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    ENV: str = "LOCAL"
    API_PREFIX: str = "/api/v1"
    INIT_COUNTER_VALUE: int = 100000000
    COUNTER_CACHE_KEY: str = "COUNTER"
    PASSWORD_SALT: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    REDIS_HOST: str = "localhost"
    REDIS_PASSWORD: str = ""
    REDIS_PORT: int = 6379
    REDIS_OM_URL: str = "localhost"
    CACHE_TTL: int = 3600

    class Config:
        env_file = ".env"

    #     env_file_encoding = "utf-8"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
