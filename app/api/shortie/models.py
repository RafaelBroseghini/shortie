from redis_om import JsonModel


class ShortenedURL(JsonModel):
    short_url: str
    long_url: str
