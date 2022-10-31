from http.client import FOUND

from fastapi import APIRouter

from app.api.analytics.models import Statistic
from app.cache.conn import RedisClientManager

router = APIRouter()


@router.get(
    "/{short_url_id}",
)
def view_number_of_clicks(short_url_id: str):
    with RedisClientManager() as cache:
        pk_analytics = cache.get(f"analytics:{short_url_id}")

        if pk_analytics:

            return Statistic.get(pk_analytics)
        return {"error": f"Shortened url [https://shortie/{short_url_id}] not found."}
