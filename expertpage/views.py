from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render

from consultation_signup.models import ConsultationSignup

from .forms import ConsultationBrowseForm


def expertpage(request):
    """Личный кабинет Параболы: список клиентов с уведомлениями"""

    # проверка пользователя
    if request.user.is_anonymous:
        return redirect("loginuser")
    if not request.user.is_expert:
        return redirect("homepage")

    # список зарегистрированных клиентов
    clients = User.objects.exclude(username="Demmenty").exclude(
        username="Parrabolla"
    )
    # новые заявки на консультацию
    new_consult_requests = ConsultationSignup.objects.filter(is_read=0)
    new_consult_signup_amount = new_consult_requests.count()

    data = {
        "clients": clients,
        "new_consult_signup_amount": new_consult_signup_amount,
    }
    return render(request, "expertpage/expertpage.html", data)


def consult_requests_page(request):
    """Управление заявками на консультацию"""

    # проверка пользователя
    if request.user.is_anonymous:
        return redirect("loginuser")
    if not request.user.is_expert:
        return redirect("homepage")

    # функция сохранения заметки к заявке консультации
    if request.POST.get("purpose") == "save":
        form = ConsultationBrowseForm(request.POST)
        if form.is_valid():
            signup_id = request.POST.get("id")
            expert_note = form.cleaned_data["expert_note"]
            instance = ConsultationSignup.objects.filter(id=signup_id)
            instance.update(expert_note=expert_note)
            result = "заметка сохранена"
        else:
            result = "данные некорректны"

        data = {
            "result": result,
        }
        return JsonResponse(data, status=200)

    # функция удаления заявки консультации
    if request.POST.get("purpose") == "delete":
        signup_id = request.POST.get("id")
        instance = ConsultationSignup.objects.filter(id=signup_id)
        instance.delete()
        data = {}
        return JsonResponse(data, status=200)

    # изменение отметки о том, что заявка прочитана
    if request.GET.get("purpose") == "make_readed":
        signup_id = request.GET.get("id")
        instance = ConsultationSignup.objects.filter(id=signup_id)
        instance.update(is_read=1)
        data = {}
        return JsonResponse(data, status=200)

    # заявки на консультацию
    consult_signup_entries = ConsultationSignup.objects.all()
    # новые заявки на консультацию
    new_consult_signup_amount = ConsultationSignup.objects.filter(
        is_read=0
    ).count()
    # формы для просмотра заявок и добавления заметки
    consult_signup_forms = []
    for entry in consult_signup_entries:
        form = ConsultationBrowseForm(instance=entry)
        consult_signup_forms.append(form)

    consult_signups_zip = zip(consult_signup_entries, consult_signup_forms)

    data = {
        "new_consult_signup_amount": new_consult_signup_amount,
        "consult_signup_entries": consult_signup_entries,
        "consult_signups_zip": consult_signups_zip,
    }
    return render(request, "expertpage/consult_requests_page.html", data)
