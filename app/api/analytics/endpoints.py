from fastapi import APIRouter

from app.api.analytics.models import Analytics
from app.api.analytics.schemas import ReadResponse

router = APIRouter()


@router.get("/{short_url_id}", response_model=ReadResponse)
async def view_number_of_clicks(short_url_id: str):
    analytics = await Analytics.find(
        Analytics.short_url_id == short_url_id
    ).first()

    if analytics:
        return ReadResponse(
            short_url_id=analytics.short_url_id,
            clicks=analytics.clicks,
            last_visited=analytics.last_visited,
        )
    return {
        "error": f"Shortened url [https://shortie/{short_url_id}] not found."
    }
