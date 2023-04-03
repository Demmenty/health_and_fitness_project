from django.contrib.auth.models import User
from django.db.models import Q

from .models import Exercise


class TrainingManager:
    """управление тренировками и упражнениями"""

    def get_exercises(client: User) -> list[Exercise]:
        """Возвращает список видов упражнений для клиента
        (среди них только созданные им лично или экспертом)"""

        expert = User.get_expert()

        exercises = Exercise.objects.filter(
            Q(author=client) | Q(author=expert)
        )

        return exercises