import datetime

from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from starlette.requests import Request
from starlette.responses import Response

from app.api.analytics.models import Statistic
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
def read(short_url_id: str, request: Request, response: Response):
    with RedisClientManager() as cache:
        now = datetime.datetime.now()

        shortened_url, short_url_analytics = (
            ShortenedURL.find(
                ShortenedURL.short_url_id == short_url_id
            ).first(),
            Statistic.find(Statistic.short_url_id == short_url_id).first(),
        )

        short_url_analytics.clicks += 1
        short_url_analytics.last_visited = now

        short_url_analytics.save()

        long_url = shortened_url.long_url

        return long_url


@router.post("")
def create(body: LongUrl, request: Request, response: Response):
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
            Statistic(short_url_id=short_url_id),
        )

        ttl = settings.CACHE_TTL
        shortened_url.save()
        shortened_url.expire(ttl)
        shortened_url_analytics.save()
        shortened_url_analytics.expire(ttl)

        return ShortenReponse(
            short_url_id=short_url_id,
            short_url=short_url,
            long_url=long_url,
            ttl=ttl,
        )


@router.put(
    "/{short_url_id}",
)
def udpate(short_url_id: str, body: LongUrl):
    shortened_url = ShortenedURL.find(
        ShortenedURL.short_url_id == short_url_id
    ).first()
    if not shortened_url:
        return {"error": f"Short url id: [{short_url_id}] not found."}
    previous_long_url, new_long_url = shortened_url.long_url, body.long_url
    short_url = shortened_url.short_url
    shortened_url.long_url = new_long_url

    shortened_url.save()

    return UpdateResponse(
        short_url_id=short_url_id,
        short_url=short_url,
        previous_long_url=previous_long_url,
        new_long_url=new_long_url,
    )


@router.delete(
    "/{short_url_id}",
)
def delete(short_url_id: str):
    shortened_url = ShortenedURL.find(
        ShortenedURL.short_url_id == short_url_id
    ).first()
    if not shortened_url:
        return {"error": f"Short url id: [{short_url_id}] not found."}

    shortened_url.delete(shortened_url.pk)

    return DeleteResponse(
        short_url_id=short_url_id,
        short_url=shortened_url.short_url,
        long_url=shortened_url.long_url,
    )
