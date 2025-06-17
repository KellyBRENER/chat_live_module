# live_chat_sse/chatMessage/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.chat_page, name="chat_page"),
    path("send/", views.send_message, name="send_message"),
    path("create_private_group/", views.create_or_get_private_group, name="create_private_group"),
    path("stream/<str:group_name>/", views.sse_chat_stream, name="sse_chat_stream"),
    path("history/<str:group_name>/", views.get_message_history, name="get_message_history"),
    path("block_user/", views.block_user, name="block_user"),
    path("unblock_user/", views.unblock_user, name="unblock_user"),
    path("get_blocked_users/", views.get_blocked_users, name="get_blocked_users"),
]
