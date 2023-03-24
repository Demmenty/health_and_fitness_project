from django.db import models
from django.contrib.auth.models import User 


@property
def is_expert(self) -> bool:
    if self.username == "Parrabolla":
        return True
    return False

User.add_to_class("is_expert", is_expert)
