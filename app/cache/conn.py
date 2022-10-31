from contextlib import contextmanager

import redis

client = redis.StrictRedis(decode_responses=True)


@contextmanager
def RedisClientManager():
    try:
        yield client
    finally:
        client.close()
