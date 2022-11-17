import base64
import datetime
import hashlib
from datetime import timezone

import jwt
from fastapi.exceptions import HTTPException
from starlette.requests import Request

import app.api.shortie.dao as ShortieDAO
import app.api.users.dao as UserDAO
from app.api.common.rate_limiter import RateLimiter
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


async def get_user_info(request: Request):
    auth_header = request.headers.get("authorization")
    token = extract_token(auth_header)
    try:
        decoded_jwt = decode_jwt(token)
        username = decoded_jwt["username"]
        return await UserDAO.find_by_username(username)
    except Exception:
        raise HTTPException(status_code=200, detail="Invalid token.")


async def is_authorized(request: Request):
    user = await get_user_info(request)
    path = request.url.path.split("/")[-1]
    short_url = await ShortieDAO.find_by_short_url_id_or_alias(path)

    if short_url.owner != user.pk:
        raise HTTPException(
            status_code=403, detail={"error": "Not authorized"}
        )
    return user


async def should_throttle(request: Request):
    user = await get_user_info(request)
    username = user.username

    r = RateLimiter(user.request_limit_per_period, user.period_seconds)
    r.incr_request_count(username)

    should_throttle = r.too_many_requests(username)

    if should_throttle:
        raise HTTPException(
            status_code=429, detail={"error": "Too many requests"}
        )
