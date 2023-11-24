from users.models import User


def get_chat_participants(request, partner_id: int | None = None) -> tuple[User, User]:
    """
    Get the chat participants for a given request.
    Logic based on the fact that chat participants are always client and expert.

    Args:
        request (HttpRequest): The request object.
        partner_id (int | None): The ID of the chat partner.
        Optional if the user is client, mandatory if the user is an expert.

    Returns:
        tuple[User, User]: A tuple containing the request user and the chat partner.
    """

    user: User = request.user
    partner = User.objects.get(id=partner_id) if user.is_expert else User.get_expert()

    return user, partner
