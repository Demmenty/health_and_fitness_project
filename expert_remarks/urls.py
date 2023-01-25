from django.urls import path
from . import views


urlpatterns = [
    path('ajax/get_commentary/', views.get_commentary, name='get_commentary'),
    path('ajax/get_commentary_form/', views.get_commentary_form, name='get_commentary_form'),
    path('ajax/mark_comment_readed/', views.mark_comment_readed, name='mark_comment_readed'),
    path('ajax/save_commentary_form/', views.save_commentary_form, name='save_commentary_form'),
    path('ajax/count_unread_comments/', views.count_unread_comments, name='count_unread_comments'),
    path('ajax/get_clientnote_form/', views.get_clientnote_form, name='get_clientnote_form'),
    path('ajax/save_clientnote_form/', views.save_clientnote_form, name='save_clientnote_form'),
    path('ajax/save_full_clientnote_form/', views.save_full_clientnote_form, name='save_full_clientnote_form'),
]
