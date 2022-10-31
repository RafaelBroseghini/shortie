from pydantic import BaseSettings


class Settings(BaseSettings):
    ENV: str = "LOCAL"
    API_PREFIX: str = "/api/v1"
    INIT_COUNTER_VALUE: int = 100000000
    COUNTER_CACHE_KEY: str = "COUNTER"
    CACHE_TTL: int = 3600


settings = Settings()
