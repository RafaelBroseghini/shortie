from typing import Optional

from aredis_om import Field, JsonModel


class ShortenedURL(JsonModel):
    short_url_id: str = Field(index=True)
    alias: Optional[str] = Field(index=True)
    short_url: str
    long_url: str
    owner: str
