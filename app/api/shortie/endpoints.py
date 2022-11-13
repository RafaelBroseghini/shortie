import asyncio
import datetime

from aredis_om import NotFoundError
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from starlette.requests import Request
from starlette.responses import Response

import app.api.analytics.dao as AnalyticsDAO
import app.api.shortie.dao as ShortieDAO
from app.api.analytics.models import Analytics
from app.api.shortie.funcs import base62encode, make_short_url
from app.api.shortie.models import ShortenedURL
from app.api.shortie.schemas import (
    DeleteResponse,
    LongUrl,
    ShortenReponse,
    UpdateResponse,
)
from app.cache.conn import RedisClientManager
from app.core.config import settings

router = APIRouter()


@router.get("/{short_url_id}", response_class=RedirectResponse)
async def read(short_url_id: str, request: Request, response: Response):
    now = datetime.datetime.now()

    try:
        shortened_url, short_url_analytics = (
            await ShortieDAO.find_by_short_url_id(short_url_id),
            await AnalyticsDAO.find_by_short_url_id(short_url_id),
        )
    except NotFoundError:
        raise HTTPException(
            status_code=404, detail={"error": "short url not found."}
        )

    short_url_analytics.clicks += 1
    short_url_analytics.last_visited = now

    await short_url_analytics.save()

    long_url = shortened_url.long_url

    return long_url


@router.post("")
async def create(body: LongUrl, request: Request, response: Response):
    with RedisClientManager() as cache:
        counter = cache.incr(settings.COUNTER_CACHE_KEY)
        short_url_id = base62encode(counter - 1)
        short_url = make_short_url(short_url_id)
        long_url = body.long_url

        shortened_url, shortened_url_analytics = (
            ShortenedURL(
                short_url_id=short_url_id,
                short_url=short_url,
                long_url=long_url,
            ),
            Analytics(short_url_id=short_url_id),
        )

        ttl = settings.CACHE_TTL
        asyncio.gather(
            shortened_url.save(),
            shortened_url.expire(ttl),
            shortened_url_analytics.save(),
            shortened_url_analytics.expire(ttl),
        )

        return ShortenReponse(
            short_url_id=short_url_id,
            short_url=short_url,
            long_url=long_url,
            ttl=ttl,
        )


@router.put(
    "/{short_url_id}",
)
async def udpate(short_url_id: str, body: LongUrl):
    try:
        shortened_url = await ShortieDAO.find_by_short_url_id(short_url_id)
    except NotFoundError:
        raise HTTPException(
            status_code=404, detail={"error": "short url not found."}
        )

    previous_long_url, new_long_url = shortened_url.long_url, body.long_url
    short_url = shortened_url.short_url
    shortened_url.long_url = new_long_url

    await shortened_url.save()

    return UpdateResponse(
        short_url_id=short_url_id,
        short_url=short_url,
        previous_long_url=previous_long_url,
        new_long_url=new_long_url,
    )


@router.delete(
    "/{short_url_id}",
)
async def delete(short_url_id: str):
    try:
        shortened_url = await ShortieDAO.find_by_short_url_id(short_url_id)
    except NotFoundError:
        raise HTTPException(
            status_code=404, detail={"error": "short url not found."}
        )
    if not shortened_url:
        return {"error": f"Short url id: [{short_url_id}] not found."}

    await shortened_url.delete(shortened_url.pk)

    return DeleteResponse(
        short_url_id=short_url_id,
        short_url=shortened_url.short_url,
        long_url=shortened_url.long_url,
    )
