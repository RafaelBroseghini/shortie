from app.api.shortie.models import ShortenedURL


async def find_by_short_url_id(short_url_id: str) -> ShortenedURL:
    return await ShortenedURL.find(
        ShortenedURL.short_url_id == short_url_id
    ).first()
