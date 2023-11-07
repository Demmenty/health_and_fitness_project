from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from home.forms import ConsultRequestForm
from users.forms import UserLoginForm


def main(request):
    """View for website main page"""

    template = "home/main.html"

    data = {
        "login_form": UserLoginForm(),
        "consult_request_form": ConsultRequestForm(),
    }
    return render(request, template, data)


@csrf_exempt
@require_http_methods(["POST"])
def save_consult_request(request):
    """Saving consultation request from users"""

    form = ConsultRequestForm(request.POST)

    if form.is_valid():
        form.save()
        return HttpResponse("Заявка получена")

    return JsonResponse(form.errors, status=400)
