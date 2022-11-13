from app.api.analytics.models import Analytics


async def find_by_short_url_id(short_url_id: str) -> Analytics:
    return await Analytics.find(Analytics.short_url_id == short_url_id).first()
