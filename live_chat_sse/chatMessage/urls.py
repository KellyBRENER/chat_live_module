# votre_application/urls.py (par exemple, chatMessage/urls.py)

from django.urls import path
from . import views

urlpatterns = [
    path("", views.chat_page, name="chat_page"),
    path("chat/send/", views.send_message, name="send_message"),
    path("chat/create_private_group/", views.create_or_get_private_group, name="create_private_group"),
    # sse_view est supprimé car le temps réel est maintenant géré par les WebSockets de Channels
]
