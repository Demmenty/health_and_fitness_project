from django.urls import path

from chat import views

urlpatterns = [
    path("msg/save", views.save_message, name="save_msg"),
    path("msg/make_read", views.make_message_read, name="make_msg_read"),
    path("msg/get_by_id", views.get_message_by_id, name="get_msg_by_id"),
    path(
        "msg/get_list_by_id",
        views.get_msgs_list_by_id,
        name="get_msgs_list_by_id",
    ),
    path("msgs/get_last", views.get_last_messages, name="get_last_msgs"),
    path("msgs/get_unread", views.get_unread_messages, name="get_unread_msgs"),
]
