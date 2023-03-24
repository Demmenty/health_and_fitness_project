from django.contrib.auth.models import User
from django.db import models


@property
def is_expert(self) -> bool:
    if self.username == "Parrabolla":
        return True
    return False


User.add_to_class("is_expert", is_expert)
