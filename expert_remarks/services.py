from .models import Commentary, Clientnote, FullClientnote
from .forms import CommentaryForm, ClientnoteForm, FullClientnoteForm
from datetime import date


def get_remark_forms(client) -> dict:
    """возвращает формы заметок и комментария, нужные для footer эксперта"""

    # комментарий для клиента
    comment_form = get_today_commentary_form(client)
    # заметка о клиенте
    monthnote_form = get_today_clientnote_form(client)
    # заметка о клиенте совокупная
    fullnote_form = get_full_clientnote_form(client)

    client_remark = {
        'comment_form': comment_form,
        'monthnote_form': monthnote_form,
        'fullnote_form': fullnote_form,
    }

    return client_remark


# комментарий от эксперта клиенту
def get_today_commentary(client):
    """возвращает объект модели комментария от эксперта за сегодня"""

    today_commentary = Commentary.objects.filter(
                        date=date.today(),
                        client=client).first()

    return today_commentary


def get_today_commentary_form(client):
    """возвращает форму для комплексного комментария клиенту от эксперта
       Дата - сегодняшняя, на другие даты меняется на странице скриптом
    """

    # форматирование для правильного отображения в инпуте
    today = date.today().strftime('%Y-%m-%d')
    try:
        instance = Commentary.objects.get(client=client, date=date.today())
        form = CommentaryForm(instance=instance, initial={'date': today})
    except Commentary.DoesNotExist:
        form = CommentaryForm(initial={'date': today})

    return form


# заметка о клиенте для эксперта (помесячная)
def get_today_clientnote_form(client):
    """Получение формы для заметки о клиенте для эксперта
       Месяц - текущий, на другие месяцы меняется на странице скриптом
    """
    
    current_month = date.today().strftime('%Y-%m')
    try:
        # месяц в модели записывается как полная дата с 1 числом
        instance = Clientnote.objects.get(client=client, date=date.today().replace(day=1))
        form = ClientnoteForm(instance=instance, initial={'date': current_month})
    except Clientnote.DoesNotExist:
        form = ClientnoteForm(initial={'date': current_month})

    return form


# заметка о клиенте для эксперта (совокупная)
def get_full_clientnote_form(client):
    """Получение формы для заметки о клиенте для эксперта совокупной"""   

    try:
        instance = FullClientnote.objects.get(client=client)
        full_clientnote_form = FullClientnoteForm(instance=instance)
    except FullClientnote.DoesNotExist:
        full_clientnote_form = FullClientnoteForm()

    return full_clientnote_form

 