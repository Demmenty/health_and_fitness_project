from users.models import User
from users.utils import get_client


def layout_context(request) -> dict[str]:
    if request.user.is_anonymous:
        return {"layout": "main/layout.html"}

    if request.user.is_expert:
        return {"layout": "expert/layout.html"}

    return {"layout": "client/layout.html"}


def client_context(request) -> dict[User | None]:
    if request.user.is_anonymous:
        return {"client": None}

    return {"client": get_client(request)}
