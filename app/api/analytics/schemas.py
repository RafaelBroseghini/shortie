from datetime import datetime

from pydantic import BaseModel


class Analytics(BaseModel):
    clicks: int = 0
    last_visited: datetime
