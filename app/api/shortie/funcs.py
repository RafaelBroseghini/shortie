from string import ascii_letters, digits

SHORTENER_MAP = ascii_letters + digits


def base62encode(number: int) -> str:
    res = []
    base = len(SHORTENER_MAP)
    while number:
        rem = number % base
        res.append(SHORTENER_MAP[rem])
        number = number // base
    return "".join(res)


def make_short_url(short_url_id: str) -> str:
    return f"https://shortie/{short_url_id}"
