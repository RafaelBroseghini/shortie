from app.api.users.models import User


async def find_by_username(username: str) -> User:
    return await User.find(User.username == username).first()


async def create(username: str, password: str) -> User:
    return await User(username=username, password=password).save()
