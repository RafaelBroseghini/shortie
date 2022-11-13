from datetime import datetime

from aredis_om import Field, JsonModel


class Analytics(JsonModel):
    short_url_id: str = Field(index=True)
    clicks: int = 0
    last_visited: datetime = None
