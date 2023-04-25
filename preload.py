from aredis_om import NotFoundError

import app.api.analytics.dao as AnalyticsDao
from app.api.analytics.models import Analytics
from app.api.shortie.dao import find_by_short_url_id_or_alias
from app.api.shortie.models import ShortenedURL
from app.api.users.dao import find_by_username
from app.api.users.models import User


async def load_users() -> None:
    try:
        await find_by_username("tortellini")
    except NotFoundError:
        user = User(
            username="tortellini",
            password="85b7ad22cd1825e5001d8bae3b2c89e2bd1647344298181fc9d62e46e60f51dc",
        )

        await user.save()


async def load_url() -> None:
    try:
        await find_by_short_url_id_or_alias("test")
    except NotFoundError:
        url = ShortenedURL(
            short_url_id="test",
            alias="testing",
            short_url=f"https://shortie/test",
            long_url="google.com",
            owner="tortellini",
        )

        await url.save()


async def load_analytics() -> None:
    try:
        await AnalyticsDao.find_by_short_url_id_or_alias("test")
    except NotFoundError:
        analytics = Analytics(
            short_url_id="test",
            alias="testing",
            clicks=0,
            owner="tortellini",
        )

        await analytics.save()
