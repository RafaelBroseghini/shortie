from app.api.users.models import User


async def load_users() -> None:
    user = User(
        username="tortellini",
        password="70c07306f309b239d84ed87c17ca8d7c2b3c0955ad24f255cf102c626be9da64",
    )

    await user.save()
