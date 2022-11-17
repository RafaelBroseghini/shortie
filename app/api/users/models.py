from aredis_om import Field, JsonModel


class User(JsonModel):
    username: str = Field(index=True)
    password: str
    role: str = "USER"
    request_limit_per_period: int = 10
    period_seconds: int = 1
