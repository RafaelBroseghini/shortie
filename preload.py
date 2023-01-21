from app.api.users.models import User


async def load_users() -> None:
    user = User(
        username="tortellini",
        password="85b7ad22cd1825e5001d8bae3b2c89e2bd1647344298181fc9d62e46e60f51dc",
    )

    await user.save()
