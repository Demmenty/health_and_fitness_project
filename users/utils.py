from users.models import User


def get_client_id(request) -> int | None:
    if request.user.is_expert:
        return request.GET.get("client_id") or request.POST.get("client_id")

    return request.user.id


def get_client(request) -> User | None:
    if request.user.is_expert:
        id = request.GET.get("client_id") or request.POST.get("client_id")
        return User.objects.filter(id=id).first()

    return request.user
