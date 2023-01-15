from django.shortcuts import redirect
from .services import *


fs_session = create_common_fs_session()


def fatsecretauth(request):
    """Привязка пользователя к его аккаунту FatSecret"""

    global fs_session

    # 1) получаем адрес подключения и направляем по нему
    if request.GET.get('oauth_verifier') is None:

        auth_url = fs_session.get_authorize_url(
                callback_url="http://127.0.0.1:8000/fatsecret_app/auth/")

        return redirect(auth_url)

    # 2) получаем ключи от FatSecret
    if request.GET.get('oauth_verifier'):

        verifier_pin = request.GET.get('oauth_verifier')

        session_token = fs_session.authenticate(verifier_pin)

        save_session_token(session_token, request.user)
        
        return redirect('mealjournal')
