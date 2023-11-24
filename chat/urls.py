from django.urls import path

from chat import views

app_name = "chat"

urlpatterns = [
    path("message/save", views.save_msg, name="save_msg"),
    path("message/set_seen", views.set_seen, name="set_seen"),
    path("messages/get_last", views.get_last_msgs, name="get_last_msgs"),
    path("messages/get_old", views.get_old_msgs, name="get_old_msgs"),
    path("messages/get_new", views.get_new_msgs, name="get_new_msgs"),
    path("messages/count_new", views.count_new_msgs, name="count_new_msgs"),
]
