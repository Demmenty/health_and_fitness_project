from django.db.models import Manager, Q, QuerySet


class MessageQuerySet(QuerySet):
    def filter_by_participants(self, user_id: int, partner_id: int):
        """
        Filter messages by chat participants.

        Args:
            user_id (int): One of the chat participants.
            partner_id (int): One of the chat participants.

        Returns:
            QuerySet: A filtered queryset of messages between two users.
        """
        return self.filter(
            Q(sender_id=user_id, recipient_id=partner_id)
            | Q(sender_id=partner_id, recipient_id=user_id)
        )


class MessageManager(Manager):
    def get_queryset(self):
        return MessageQuerySet(self.model, using=self._db)

    def filter_by_participants(self, user_id: int, partner_id: int):
        """
        Filter messages by chat participants.

        Args:
            user_id (int): One of the chat participants.
            partner_id (int): One of the chat participants.

        Returns:
            QuerySet: A filtered queryset of messages between two users.
        """
        return self.get_queryset().filter_by_participants(user_id, partner_id)
