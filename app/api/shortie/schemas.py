from typing import Optional

from pydantic import BaseModel


class LongUrl(BaseModel):
    long_url: str
    alias: Optional[str]


class ShortenReponse(LongUrl):
    short_url_id: str
    short_url: str


class UpdateResponse(BaseModel):
    short_url_id: str
    short_url: str
    previous_long_url: str
    new_long_url: str


class DeleteResponse(BaseModel):
    short_url_id: str
    short_url: str
    long_url: str
    operation: str = "DELETE"
