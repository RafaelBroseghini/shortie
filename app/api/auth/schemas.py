from pydantic import BaseModel, validator


class SignUp(BaseModel):
    username: str
    password: str

    @validator("username", "password")
    def larger_than_eight_characters(cls, value: str):
        if len(value) <= 8:
            raise ValueError(f"'{value}' must be greater than 8 characters.")
        return value
