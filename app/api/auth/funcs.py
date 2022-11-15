import base64
import datetime
import hashlib
from datetime import timezone

import jwt
from fastapi.exceptions import HTTPException
from starlette.requests import Request

from app.api.users.models import User
from app.core.config import settings


def build_payload(user: User) -> dict:
    return {
        "user_id": user.pk,
        "username": user.username,
        "role": user.role,
        "exp": one_hour_from_now(),
    }


def decode_credentials(request: Request):
    auth_header = request.headers.get("authorization")

    _, encoded_credentials = auth_header.split("Basic ")

    credentials = base64.b64decode(encoded_credentials).decode("utf-8")

    username, password = credentials.split(":", 1)

    encrypted_password = salt_and_sha256_encrypt(password)

    return username, encrypted_password


def salt_and_sha256_encrypt(password: str) -> str:
    salted_password = "".join([password, settings.PASSWORD_SALT])
    return hashlib.sha256(salted_password.encode("utf-8")).hexdigest()


def one_hour_from_now():
    return datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(
        seconds=3600
    )


def encode_jwt(payload: dict) -> str:
    return jwt.encode(
        payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )


def decode_jwt(encoded_jwt: str) -> dict:
    return jwt.decode(
        encoded_jwt, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
    )


def extract_token(encoded_jwt: str) -> str:
    return encoded_jwt.split("Bearer ")[1]


def get_user_info(request: Request):
    auth_header = request.headers.get("authorization")
    token = extract_token(auth_header)
    try:
        return decode_jwt(token)
    except Exception:
        raise HTTPException(status_code=200, detail="Invalid token.")
