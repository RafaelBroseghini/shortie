import asyncio
import datetime

import qrcode
import requests
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from starlette.requests import Request
from starlette.responses import Response

import app.api.analytics.dao as AnalyticsDAO
import app.api.shortie.dao as ShortieDAO
from app.api.analytics.models import Analytics
from app.api.auth.funcs import is_authorized, should_throttle
from app.api.shortie.funcs import base62encode, make_short_url
from app.api.shortie.models import ShortenedURL
from app.api.shortie.schemas import (
    DeleteResponse,
    LongUrl,
    ShortenReponse,
    ShortUrlId,
    UpdateResponse,
)
from app.api.users.models import User
from app.cache.conn import RedisClientManager
from app.core.config import get_settings

settings = get_settings()

router = APIRouter()


@router.get("/{short_url_id}", response_class=RedirectResponse)
async def read(short_url_id: str, request: Request, response: Response):
    now = datetime.datetime.now()

    shortened_url, short_url_analytics = (
        await ShortieDAO.find_by_short_url_id_or_alias(short_url_id),
        await AnalyticsDAO.find_by_short_url_id_or_alias(short_url_id),
    )

    short_url_analytics.clicks += 1
    short_url_analytics.last_visited = now

    await short_url_analytics.save()

    long_url = shortened_url.long_url

    if not (long_url.startswith("https://") or long_url.startswith("http://")):
        try:
            schemes = ["https://", "http://"]
            for scheme in schemes:
                r = requests.head(scheme + long_url)
                if r.status_code < 400:
                    return RedirectResponse(scheme + long_url)
        except requests.exceptions.RequestException:
            pass

    return RedirectResponse(long_url)


@router.post("")
async def create(
    body: LongUrl,
    request: Request,
    user: User | None = Depends(should_throttle),
):
    with RedisClientManager() as cache:
        counter = cache.incr(settings.COUNTER_CACHE_KEY)
        short_url_id = base62encode(counter - 1)
        short_url = make_short_url(short_url_id)
        alias, long_url = body.alias, body.long_url
        if user:
            user_pk = user.pk
        else:
            user_pk = None
            if request.client:
                user_pk = request.client.host

        if alias and await ShortieDAO.alias_already_exists(alias):
            return JSONResponse(
                status_code=200,
                content={"error": f"alias {alias} is already taken."},
            )

        shortened_url, shortened_url_analytics = (
            ShortenedURL(
                short_url_id=short_url_id,
                alias=alias,
                short_url=short_url,
                long_url=long_url,
                owner=user_pk,
            ),
            Analytics(
                short_url_id=short_url_id,
                alias=alias,
                owner=user_pk,
            ),
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
            alias=alias,
            short_url=short_url,
            long_url=long_url,
        )


@router.put("/{short_url_id}", dependencies=[Depends(is_authorized)])
async def udpate(short_url_id: str, body: LongUrl):
    shortened_url = await ShortieDAO.find_by_short_url_id(short_url_id)

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


@router.delete("/{short_url_id}", dependencies=[Depends(is_authorized)])
async def delete(short_url_id: str):
    shortened_url = await ShortieDAO.find_by_short_url_id(short_url_id)

    await shortened_url.delete(shortened_url.pk)

    return DeleteResponse(
        short_url_id=short_url_id,
        short_url=shortened_url.short_url,
        long_url=shortened_url.long_url,
    )


@router.post("/qr", response_class=FileResponse)
async def qr(body: ShortUrlId):
    short_url = await ShortieDAO.find_by_short_url_id_or_alias(
        body.short_url_id
    )

    # TODO: change to deployed host/short_url_id
    img = qrcode.make(short_url.long_url)

    filename = f"/tmp/{body.short_url_id}.png"

    img.save(filename)

    return FileResponse(filename)
