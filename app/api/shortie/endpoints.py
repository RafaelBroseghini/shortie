import datetime

import pip
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from starlette.requests import Request
from starlette.responses import Response

from app.api.analytics.models import Statistic
from app.api.shortie.funcs import base62encode
from app.api.shortie.models import ShortenedURL
from app.api.shortie.schemas import LongUrl, ShortenReponse
from app.cache.conn import RedisClientManager
from app.cache.schemas import key_schemas
from app.core.config import settings

router = APIRouter()


@router.get("/{short_url_id}", response_class=RedirectResponse)
def read_long_url(short_url_id: str, request: Request, response: Response):
    with RedisClientManager() as cache:
        now = datetime.datetime.now()

        pk_url = cache.get(f"{short_url_id}")
        pk_analytics = cache.get(f"analytics:{short_url_id}")

        short_url, short_url_analytics = ShortenedURL.get(pk_url), Statistic.get(
            pk_analytics
        )

        short_url_analytics.clicks += 1
        short_url_analytics.last_visited = now

        short_url_analytics.save()

        long_url = short_url.dict().get("long_url")

        return long_url


@router.post("")
def shorten_url(body: LongUrl, request: Request, response: Response):
    with RedisClientManager() as cache:
        counter = cache.incr("counter")
        long_url = body.url

        encoded_url = base62encode(counter - 1)

        shortened_url, shortened_url_analytics = (
            ShortenedURL(short_url=encoded_url, long_url=long_url),
            Statistic(),
        )
        pk_url, pk_analytics = (
            shortened_url.pk,
            shortened_url_analytics.pk,
        )

        pipeline = cache.pipeline()
        pipeline.set(encoded_url, pk_url, ex=settings.CACHE_TTL).set(
            f"analytics:{encoded_url}", pk_analytics
        )
        pipeline.execute()

        shortened_url.save()
        shortened_url_analytics.save()
        shortened_url.expire(settings.CACHE_TTL)

        return ShortenedURL.get(pk_url)
