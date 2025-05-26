from django.urls import re_path
from . import consumers

#liste d'URL de websocket que django utilisera
websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
