from app.api.shortie.models import ShortenedURL


async def find_by_short_url_id(short_url_id: str) -> ShortenedURL:
    return await ShortenedURL.find(
        ShortenedURL.short_url_id == short_url_id
    ).first()


async def find_by_short_url_id_or_alias(short_url_id: str) -> ShortenedURL:
    return await ShortenedURL.find(
        (ShortenedURL.short_url_id == short_url_id)
        | (ShortenedURL.alias == short_url_id)
    ).first()


async def alias_already_exists(alias: str) -> ShortenedURL:
    return await ShortenedURL.find(ShortenedURL.alias == alias).count()


async def find_by_alias(alias: str) -> ShortenedURL:
    return await ShortenedURL.find(ShortenedURL.alias == alias).first()
