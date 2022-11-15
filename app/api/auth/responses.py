from fastapi.responses import JSONResponse


class AuthFailedResponse:
    def __new__(self):
        return JSONResponse(
            status_code=200,
            content={
                "error": "Username and password combination could not be found."
            },
        )


class UserAlreadyExistsResponse:
    def __new__(self):
        return JSONResponse(
            status_code=200,
            content={"error": "Username is already taken."},
        )


class JWTResponse:
    def __new__(self, encoded_jwt):
        return {"access_token": encoded_jwt}


class SignUpSuccessResponse:
    def __new__(self):
        return JSONResponse(
            status_code=200,
            content={"success": "Success sign up!"},
        )
