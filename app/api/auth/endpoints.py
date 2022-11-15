from aredis_om import NotFoundError
from fastapi import APIRouter
from starlette.requests import Request

import app.api.users.dao as UserDAO
from app.api.auth.funcs import (
    build_payload,
    decode_credentials,
    encode_jwt,
    salt_and_sha256_encrypt,
)
from app.api.auth.responses import (
    AuthFailedResponse,
    JWTResponse,
    SignUpSuccessResponse,
    UserAlreadyExistsResponse,
)
from app.api.auth.schemas import SignUp

router = APIRouter()


@router.get("/login")
async def login(request: Request):
    username, password = decode_credentials(request)

    try:
        user = await UserDAO.find_by_username(username)

        if password == user.password:
            payload = build_payload(user)

            encoded = encode_jwt(payload)

            return JWTResponse(encoded)
        else:
            return AuthFailedResponse()
    except NotFoundError:
        return AuthFailedResponse()


@router.post("/signup")
async def signup(body: SignUp):
    username, password = body.username, body.password
    try:
        await UserDAO.find_by_username(username)
        return UserAlreadyExistsResponse()
    except NotFoundError:
        encrypted_password = salt_and_sha256_encrypt(password)
        await UserDAO.create(username, encrypted_password)

    return SignUpSuccessResponse()
