from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ReadResponse(BaseModel):
    short_url_id: str
    clicks: int = 0
    last_visited: Optional[datetime]
