from datetime import datetime

from pydantic import validator
from redis_om import JsonModel


class Statistic(JsonModel):
    clicks: int = 0
    last_visited: datetime = None
