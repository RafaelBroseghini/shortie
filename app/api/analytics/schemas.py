from datetime import datetime

from pydantic import BaseModel


class ReadResponse(BaseModel):
    short_url_id: str
    clicks: int = 0
    last_visited: datetime | None
