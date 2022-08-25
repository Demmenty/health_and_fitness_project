from django.shortcuts import render, redirect

# Create your views here.
def controlpage(request):
    """Личный кабинет Параболы"""

    # если аноним - пусть регается
    if request.user.is_anonymous:
        return redirect('loginuser')

    data = {}

    return render(request, 'controlpage/controlpage.html', data)
