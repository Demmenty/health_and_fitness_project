from django.shortcuts import render, redirect
from expert_remarks.services import get_today_commentary
from client_info.services import get_clientmemo_form_for


def training(request):
    """Страница для контроля тренировок"""

    # проверка пользователя
    if request.user.is_anonymous:
        return redirect("loginuser")
    if request.user.username == "Parrabolla":
        return redirect("expertpage")

    clientmemo_form = get_clientmemo_form_for(request.user)

    # комментарий за сегодня от эксперта
    today_commentary = get_today_commentary(request.user)

    data = {
        "clientmemo_form": clientmemo_form,
        "today_commentary": today_commentary,
    }
    return render(request, "training/training.html", data)