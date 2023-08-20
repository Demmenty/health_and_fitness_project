from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from expert_overview.forms import ConsultationsignupForm


@csrf_exempt
@require_http_methods(["POST"])
def save_consultation_signup(request):
    """Сохранение формы заявки на консультацию через аякс"""

    form = ConsultationsignupForm(request.POST)

    if form.is_valid():
        form.save()
        return HttpResponse("Заявка получена")

    return JsonResponse(form.errors, status=400)
