from django.contrib.auth.models import User


@property
def is_expert(self) -> bool:
    if self.username == "Parrabolla":
        return True
    return False


@staticmethod
def get_expert() -> User:
    expert = User.objects.get(username="Parrabolla")
    return expert


User.add_to_class("is_expert", is_expert)
User.add_to_class("get_expert", get_expert)
