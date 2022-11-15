from aredis_om import Field, JsonModel


class User(JsonModel):
    username: str = Field(index=True)
    password: str
    role: str = "USER"
