from fastapi import FastAPI

from app.cache.conn import RedisClientManager
from app.core.config import settings
from app.router import api_router

app = FastAPI(debug=True, name="Shortie - Link Shrtnr :)")

app.include_router(api_router)


@app.on_event("startup")
async def startup_event():
    if settings.ENV == "LOCAL":
        with RedisClientManager() as cache:
            cache.flushdb()
            cache.set(settings.COUNTER_CACHE_KEY, settings.INIT_COUNTER_VALUE)
