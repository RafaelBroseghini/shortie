from pydantic import BaseModel


class LongUrl(BaseModel):
    url: str


class ShortenReponse(LongUrl):
    short_url: str
    ttl: int
