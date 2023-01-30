from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import ConsultationsignupForm
from django.http import JsonResponse


@csrf_exempt
def save_consultation_signup(request):
    """Сохранение формы заявки на консультацию через аякс"""

    if request.method == 'POST':
        form = ConsultationsignupForm(request.POST)
        if form.is_valid():
            form.save()
            result = 'Заявка получена'
        else:
            result = form.errors
        data = {
            'result': result,
        }
        return JsonResponse(data, status=200)
    else:
        return redirect('homepage')
