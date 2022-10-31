from unicodedata import name

from fastapi import FastAPI

from app.cache.conn import RedisClientManager
from app.router import api_router

app = FastAPI(debug=True, name="Shortie - Link Shrtnr :)")

app.include_router(api_router)


@app.on_event("startup")
async def startup_event():
    with RedisClientManager() as cache:
        cache.flushdb()
        cache.set("counter", 100000000)
