from users.models import User


def get_client_id(request) -> int | None:
    """
    Returns a client ID depending on request user type.

    Returns:
        int | None: The ID of the client.
            If user is expert, "client_id" must be passed in GET or POST!
            If user is not expert, returns authenticated user ID
    """

    if request.user.is_expert:
        client_id = request.GET.get("client_id") or request.POST.get("client_id")
    else:
        client_id = request.user.id

    return client_id


def get_client(request) -> User | None:
    """
    Returns a User object depending on request user type.

    (If user is expert, "client_id" must be passed in GET or POST!)
    """

    if request.user.is_expert:
        id = request.GET.get("client_id") or request.POST.get("client_id")
        return User.objects.filter(id=id).first()

    return request.user


def email_exists(email: str) -> bool:
    """
    Check if an email exists in the database.

    Args:
        email (str): The email to check.

    Returns:
        bool: True if the email exists in the User model with is_active=True, False otherwise.
    """

    return User.objects.filter(email=email.lower(), is_active=True).exists()
