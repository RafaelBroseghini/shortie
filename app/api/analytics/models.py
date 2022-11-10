from datetime import datetime

from redis_om import JsonModel, Field


class Statistic(JsonModel):
    short_url_id: str = Field(index=True)
    clicks: int = 0
    last_visited: datetime = None
