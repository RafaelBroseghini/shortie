import datetime

from app.cache.conn import client


class RateLimiter:
    key = "request-count"

    def __init__(self, rate_limit, period):
        self.client = client
        self.rate_limit = rate_limit
        self.period = period

    @classmethod
    def user_key(cls, user):
        return f"{user}:{cls.key}"

    @classmethod
    def now(cls) -> datetime.datetime:
        return datetime.datetime.now(tz=datetime.timezone.utc)

    @classmethod
    def period_ago(cls, period: int):
        return datetime.timedelta(seconds=period)

    def incr_request_count(self, user):
        now = RateLimiter.now().timestamp()
        user_limiter_key = self.user_key(user)
        self.client.zadd(user_limiter_key, {str(now): now})

    def too_many_requests(self, user):
        user_limiter_key = self.user_key(user)

        now = RateLimiter.now()
        now_ts = now.timestamp()

        period_ago = RateLimiter.period_ago(self.period)
        period_ago_ts = (now - period_ago).timestamp()

        requests = self.client.zrevrangebyscore(
            user_limiter_key, now_ts, period_ago_ts
        )

        self.client.zremrangebyscore(user_limiter_key, 0, period_ago_ts - 1)

        if len(requests) > self.rate_limit:
            return True

        return False
