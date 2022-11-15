from aredis_om import Migrator, NotFoundError
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from redis.exceptions import ConnectionError
from starlette.requests import Request

from app.cache.conn import RedisClientManager
from app.core.config import settings
from app.router import api_router
from preload import load_users

app = FastAPI(debug=True, name="Shortie - Link Shrtnr :)")

app.include_router(api_router)


@app.exception_handler(ConnectionError)
async def conn_error_callback(request: Request, exc: Exception):
    return JSONResponse({"detail": "Connection refused."}, status_code=500)


@app.exception_handler(NotFoundError)
async def data_store_obj_not_found_callback(request: Request, exc: Exception):
    return JSONResponse({"detail": "Short URL not found :("}, status_code=500)


@app.on_event("startup")
async def startup_event():
    if settings.ENV == "LOCAL":
        with RedisClientManager() as cache:
            cache.flushdb()
            cache.set(settings.COUNTER_CACHE_KEY, settings.INIT_COUNTER_VALUE)
        await Migrator().run()
        await load_users()
