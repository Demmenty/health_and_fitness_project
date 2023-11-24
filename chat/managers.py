from django.db.models import Manager, Q, QuerySet

from users.models import User


class MessageQuerySet(QuerySet):
    def filter_by_participants(self, user: User, partner: User):
        """
        Filter messages by chat participants.

        Args:
            user (User): One of the chat participants.
            partner (User): One of the chat participants.

        Returns:
            QuerySet: A filtered queryset of messages between two users.
        """
        return self.filter(
            Q(sender=user, recipient=partner) | Q(sender=partner, recipient=user)
        )


class MessageManager(Manager):
    def get_queryset(self):
        return MessageQuerySet(self.model, using=self._db)

    def filter_by_participants(self, user: User, partner: User):
        """
        Filter messages by chat participants.

        Args:
            user (User): One of the chat participants.
            partner (User): One of the chat participants.

        Returns:
            QuerySet: A filtered queryset of messages between two users.
        """
        return self.get_queryset().filter_by_participants(user, partner)
