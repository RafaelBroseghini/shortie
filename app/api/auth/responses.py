from fastapi.responses import JSONResponse


class AuthFailedResponse:
    def __new__(cls):
        return JSONResponse(
            status_code=200,
            content={"error": "Username and password combination could not be found."},
        )


class MissingCredentialsResponse:
    def __new__(cls):
        return JSONResponse(
            status_code=200,
            content={"error": "Missing credentials."},
        )


class UserAlreadyExistsResponse:
    def __new__(cls):
        return JSONResponse(
            status_code=200,
            content={"error": "Username is already taken."},
        )


class JWTResponse:
    def __new__(cls, encoded_jwt):
        return {"access_token": encoded_jwt}


class SignUpSuccessResponse:
    def __new__(cls):
        return JSONResponse(
            status_code=200,
            content={"success": "Success sign up!"},
        )
