from contextlib import contextmanager

import redis

from app.core.config import settings

client = redis.StrictRedis(decode_responses=True, host=settings.REDIS_HOST)


@contextmanager
def RedisClientManager():
    try:
        yield client
    finally:
        client.close()
