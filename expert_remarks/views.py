from django.http import JsonResponse
from django.db.models import Q
from .models import Commentary, Clientnote, FullClientnote
from .forms import CommentaryForm, ClientnoteForm, FullClientnoteForm


# комментарии от эксперта клиенту
def get_commentary_form(request):
    """Получение формы коммента клиенту для эксперта
       для выбранной на странице даты через скрипт в layout"""

    if request.user.username != 'Parrabolla':
        data = {}
        return JsonResponse(data, status=403)

    client_id = request.GET.get('client_id', None)
    comment_date = request.GET['date']

    try:
        instance = Commentary.objects.get(client=client_id, date=comment_date)
        data = {
            'general': instance.general,
            'measurements': instance.measurements,
            'nutrition': instance.nutrition,
            'workout': instance.workout,
        }
    except Commentary.DoesNotExist:
        data = {
        'general': '',
        'measurements': '',
        'nutrition': '',
        'workout': '',
        }

    return JsonResponse(data, status=200)


def save_commentary_form(request):
    """Сохранение формы коммента для клиента через аякс-скрипт
       Используется в controlpage/layout.html
    """
    if request.user.username != 'Parrabolla':
        data = {}
        return JsonResponse(data, status=403)

    if request.method == 'POST':
        client_id = request.POST['client']
        form = CommentaryForm(request.POST)

        if form.is_valid():
            comment_date = form.cleaned_data['date']

            try:
                instance = Commentary.objects.get(client=client_id, date=comment_date)
                form = CommentaryForm(request.POST, instance=instance)
                form = form.save(commit=False)
            except Commentary.DoesNotExist:
                form = form.save(commit=False)
                form.client_id = client_id

            # если поле не пусто, то оставить флаг о непрочитанности
            form.general_read = not bool(form.general)
            form.measurements_read = not bool(form.measurements)
            form.nutrition_read = not bool(form.nutrition)
            form.workout_read = not bool(form.workout)

            form.save()
            result = 'комментарий сохранен'
        
        else:
            result = 'данные некорректны'

        data = {
            'result': result,
        }
        return JsonResponse(data, status=200)


# 
def get_commentary(request):
    """Получение данных комментария клиенту для клиента
       для выбранной на странице даты через скрипт в layout"""

    if request.user.is_anonymous:
        return JsonResponse({}, status=403)

    client_id = request.user.id
    comment_date = request.GET['date']

    try:
        instance = Commentary.objects.get(client=client_id, date=comment_date)
        data = {
            'general': instance.general,
            'measurements': instance.measurements,
            'nutrition': instance.nutrition,
            'workout': instance.workout,
            'general_read': instance.general_read,
            'measurements_read': instance.measurements_read,
            'nutrition_read': instance.nutrition_read,
            'workout_read': instance.workout_read,
        }
    except Commentary.DoesNotExist:
        data = {
        'general': '',
        'measurements': '',
        'nutrition': '',
        'workout': '',
        'general_read': True,
        'measurements_read': True,
        'nutrition_read': True,
        'workout_read': True,
        }

    return JsonResponse(data, status=200)


def mark_comment_readed(request):
    """Запись инфо о том, что коммент прочитан клиентом
       через скрипт в layout"""
    if request.user.is_anonymous:
        data = {}
        return JsonResponse(data, status=403)

    client_id = request.user.id
    comment_date = request.GET['date']
    labelname = request.GET['label']

    # сюда не попадут запросы о несуществующих
    # из-за фильтра в javascript - controlLabelReaded()
    commentary = Commentary.objects.get(client=client_id, date=comment_date)

    if labelname == 'general':
        commentary.general_read = True
    elif labelname == 'measurements':
        commentary.measurements_read = True
    elif labelname == 'nutrition':
        commentary.nutrition_read = True
    elif labelname == 'workout':
        commentary.workout_read = True
    
    commentary.save()

    data = {}

    return JsonResponse(data, status=200)


def count_unread_comments(request):
    """ получение количества непрочитаных комментов 
    через скрипт в layout"""
    if request.user.is_anonymous:
        data = {}
        return JsonResponse(data, status=403)

    unread_comments = Commentary.objects.filter(
        Q(client=request.user), 
        Q(general_read=0) | Q(measurements_read=0) | Q(nutrition_read=0) | Q(workout_read=0) 
    )
    count_of_unread = unread_comments.count()

    data = {
        'count_of_unread': count_of_unread,
    }
    return JsonResponse(data, status=200)


# заметки о клиенте для эксперта (помесячная)
def get_clientnote_form(request):
    """Получение формы коммента клиенту для эксперта
       для выбранной на странице даты через скрипт в layout"""

    if request.user.username != 'Parrabolla':
        data = {}
        return JsonResponse(data, status=403)

    client_id = request.GET['client_id']
    clientnote_date = request.GET['date'] + '-01'

    try:
        instance = Clientnote.objects.get(client=client_id, date=clientnote_date)
        data = {
            'general': instance.general,
            'measurements': instance.measurements,
            'nutrition': instance.nutrition,
            'workout': instance.workout,
        }
    except Clientnote.DoesNotExist:
        data = {
        'general': '',
        'measurements': '',
        'nutrition': '',
        'workout': '',
        }

    return JsonResponse(data, status=200)


def save_clientnote_form(request):
    """Сохранение формы заметки о клиенте через аякс-скрипт"""
    if request.user.username != 'Parrabolla':
        data = {}
        return JsonResponse(data, status=403)

    if request.method == 'POST':
        client_id = request.POST['client']
        form = ClientnoteForm(request.POST)

        if form.is_valid():
            clientnote_date = form.cleaned_data['date']
            try:
                instance = Clientnote.objects.get(client=client_id, date=clientnote_date)
                form = ClientnoteForm(request.POST, instance=instance)
                form.save()
            except Clientnote.DoesNotExist:
                form.save()
            result = 'заметка сохранена'
        else:
            result = 'данные некорректны'

        data = {
            'result': result,
        }
        return JsonResponse(data, status=200)
    

# заметки о клиенте для эксперта (совокупная)
def save_full_clientnote_form(request):
    """Сохранение формы совокупной заметки о клиенте через аякс-скрипт"""
    if request.user.username != 'Parrabolla':
        data = {}
        return JsonResponse(data, status=403)

    if request.method == 'POST':
        client_id = request.POST['client']
        form = FullClientnoteForm(request.POST)

        if form.is_valid():
            try:
                instance = FullClientnote.objects.get(client=client_id)
                form = FullClientnoteForm(request.POST, instance=instance)
                form.save()
            except FullClientnote.DoesNotExist:
                form.save()
            result = 'заметка сохранена'
        else:
            result = 'данные некорректны'

        data = {
            'result': result,
        }
        return JsonResponse(data, status=200)
    