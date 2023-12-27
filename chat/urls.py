from django.urls import path

from chat import ajax, views

app_name = "chat"

urlpatterns = [
    path("", views.chat, name="chat"),
    path("message/save", ajax.save_msg, name="save_msg"),
    path("message/set_seen", ajax.set_seen, name="set_seen"),
    path("messages/get_last", ajax.get_last_msgs, name="get_last_msgs"),
    path("messages/get_old", ajax.get_old_msgs, name="get_old_msgs"),
    path("messages/get_new", ajax.get_new_msgs, name="get_new_msgs"),
    path("messages/count_new", ajax.count_new_msgs, name="count_new_msgs"),
]
